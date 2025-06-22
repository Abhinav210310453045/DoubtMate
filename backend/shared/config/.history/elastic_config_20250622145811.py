from elasticsearch import Elasticsearch, exceptions, helpers

class ElasticCRUD:
    def __init__(self, host="http://localhost:9200"):
        self.es = Elasticsearch(hosts=[host])

    # INDEX OPERATIONS
    def create_index(self, index_name, mappings=None):
        if not self.es.indices.exists(index=index_name):
            self.es.indices.create(index=index_name, body=mappings or {})
            print(f"Index '{index_name}' created.")
        else:
            print(f"Index '{index_name}' already exists.")

    def delete_index(self, index_name):
        if self.es.indices.exists(index=index_name):
            self.es.indices.delete(index=index_name)
            print(f"Index '{index_name}' deleted.")

    # INSERT OPERATIONS
    def insert_one(self, index, doc_id, doc):
        return self.es.index(index=index, id=doc_id, body=doc)

    def insert_many(self, index, docs: list):
        actions = [
            {"_index": index, "_source": doc} for doc in docs
        ]
        return helpers.bulk(self.es, actions)

    # READ OPERATIONS
    def get_one(self, index, doc_id):
        try:
            return self.es.get(index=index, id=doc_id)['_source']
        except exceptions.NotFoundError:
            return None

    def get_all(self, index):
        query = {"query": {"match_all": {}}}
        return self._scroll_search(index, query)

    def search(self, index, query_dict):
        return self._scroll_search(index, {"query": query_dict})

    def search_by_field(self, index, field, value):
        query = {"match": {field: value}}
        return self.search(index, query)

    # UPDATE OPERATIONS
    def update_one(self, index, doc_id, fields_to_update):
        return self.es.update(index=index, id=doc_id, body={"doc": fields_to_update})

    def update_many(self, index, query_dict, fields_to_update):
        script = " ; ".join([f"ctx._source.{k} = '{v}'" for k, v in fields_to_update.items()])
        query = {
            "script": {"source": script},
            "query": query_dict
        }
        return self.es.update_by_query(index=index, body=query)

    # DELETE OPERATIONS
    def delete_one(self, index, doc_id):
        try:
            return self.es.delete(index=index, id=doc_id)
        except exceptions.NotFoundError:
            return {"result": "not_found"}

    def delete_many(self, index, query_dict):
        query = {"query": query_dict}
        return self.es.delete_by_query(index=index, body=query)

    # INTERNAL SCROLL SEARCH (for large results)
    def _scroll_search(self, index, query, scroll='2m', size=1000):
        result = helpers.scan(self.es, index=index, query=query, scroll=scroll, size=size)
        return [doc['_source'] for doc in result]
