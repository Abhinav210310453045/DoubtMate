# import fitz  # PyMuPDF
# import pdfplumber
# import os
# from pdfminer.high_level import extract_text
# from pdfminer.high_level import extract_pages
# from pdfminer.layout import LTTextContainer

# class DataExtract:
#     def __init__(self, pdf_path, tool_name):
#         self.pdf_path = pdf_path
#         self.pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
#         self.text_folder = f"{self.pdf_name}_text_{tool_name}"
#         os.makedirs(self.text_folder, exist_ok=True)  # Create main folder


#     def extract_text_pymupdf(self):
#         """Extract text using PyMuPDF and save it."""
#         doc = fitz.open(self.pdf_path)
#         text_file_path = os.path.join(self.text_folder, "pymupdf_extracted_text.txt")
#         with open(text_file_path, "w", encoding="utf-8") as text_file:
#             for page_num in range(len(doc)):
#                 page = doc[page_num]
#                 text = page.get_text("text")
#                 text_file.write(f"\n\nPage {page_num + 1}\n{text}")
#         print(f"Saved: {text_file_path}")

    # def extract_text_pdfminer(self):
    #     """Extract text using PDFMiner and save it."""
    #     text = extract_text(self.pdf_path)
    #     text_file_path = os.path.join(self.text_folder, "pdfminer_extracted_text.txt")
    #     with open(text_file_path, "w", encoding="utf-8") as text_file:
    #         text_file.write(text)
    #     print(f"Saved: {text_file_path}")
   

#     def extract_text_pdfminer(self):
#         """Extract text using PDFMiner, preserving page breaks."""
#         text_file_path = os.path.join(self.text_folder, "pdfminer_extracted_text.txt")
        
#         with open(text_file_path, "w", encoding="utf-8") as text_file:
#             for page_num, page_layout in enumerate(extract_pages(self.pdf_path), start=1):
#                 text_file.write(f"\n\nPage {page_num}\n")  # Page separator
#                 for element in page_layout:
#                     if isinstance(element, LTTextContainer):  # Extract only text elements
#                         text_file.write(element.get_text())
        
#         print(f"Saved: {text_file_path}")

#     def extract_text_pdfplumber(self):
#         """Extract text using pdfplumber and save it."""
#         text_file_path = os.path.join(self.text_folder, "pdfplumber_extracted_text.txt")
#         with open(text_file_path, "w", encoding="utf-8") as text_file:
#             with pdfplumber.open(self.pdf_path) as pdf:
#                 for page_num, page in enumerate(pdf.pages):
#                     text = page.extract_text()
#                     if text:
#                         text_file.write(f"\n\nPage {page_num + 1}\n{text}")
#         print(f"Saved: {text_file_path}")

#     def run(self):
#         """Run text extraction using all three methods."""
#         # self.extract_text_pymupdf()
#         self.extract_text_pdfminer()
#         # self.extract_text_pdfplumber()
#         print("Text extraction completed.")

# # Usage Example:
# # pdf_extractor = DataExtract("example.pdf")
# # pdf_extractor.run()

import os
import threading
from concurrent.futures import ThreadPoolExecutor
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer

class DataExtract:
    def __init__(self, pdf_path, tool_name, max_workers=4):
        self.pdf_path = pdf_path
        self.pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        self.text_folder = f"{self.pdf_name}_text_{tool_name}"
        self.max_workers = max_workers
        os.makedirs(self.text_folder, exist_ok=True)

    def _extract_page(self, page_num, page_layout):
        """Extract text from a single page and save it to a file."""
        print(f"Processing Page {page_num} on Thread: {threading.current_thread().name}")  # ✅ Check thread

        page_folder = os.path.join(self.text_folder, f"page_{page_num}")
        os.makedirs(page_folder, exist_ok=True)  # Create subfolder for each page

        text_file_path = os.path.join(page_folder, f"page_{page_num}.txt")

        with open(text_file_path, "w", encoding="utf-8") as text_file:
            text_file.write(f"Page {page_num}\n\n")  # Add page header
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    text_file.write(element.get_text())  # Write text content

        print(f"Saved: {text_file_path}")

    def extract_text_pdfminer(self):
        """Extract text using multi-threading for efficiency."""
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            for page_num, page_layout in enumerate(extract_pages(self.pdf_path), start=1):
                futures.append(executor.submit(self._extract_page, page_num, page_layout))

            
            print(f"Total Active Threads: {threading.active_count()}")

            # Wait for all threads to complete
            for future in futures:
                future.result()


