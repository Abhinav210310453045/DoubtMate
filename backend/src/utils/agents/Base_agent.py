import os
from dotenv import load_dotenv
from langchain_groq.chat_models import ChatGroq

class BaseAgent:
    def __init__(self,name):
        self.name=name
        load_dotenv()
        # self.model='deepseek-r1-distill-llama-70b'
        self.model='llama-3.3-70b-versatile'
        os.environ['LANGCHAIN_TRACING_V2'] = 'true'
        self.llm=ChatGroq(
            model=self.model,
            temperature=0,
            max_tokens=600,
            max_retries=3
        )
        




    
        
        