from src.utils.agents.text_extractor import DataExtract

def main():
    pdf_path = "DataBase/jesc101.pdf"  # Replace with actual PDF path
    tool_name = "pdfminer"

    extractor = DataExtract(pdf_path, tool_name, max_workers=8)  # Adjust workers as needed
    extractor.extract_text_pdfminer()

if __name__ == "__main__":
    main()


# # if __name__=="__main__":
# #     main()

# from ollama_ocr import OCRProcessor

# # Create an instance with the new model
# ocr = OCRProcessor(model_name='granite3.2-vision')

# # Process a PDF file
# result = ocr.process_image(
#     image_path="DataBase/jesc101.pdf",  # Replace with your PDF file path
#     format_type="text",           # Options: markdown, text, json, structured, key_value, table
#     language="eng"                # Specify language if supported by the model
#     #custom_prompt= ""            # overwrite the default format type
# )

# print(result)


# from ollama_ocr import OCRProcessor
# import os
# import subprocess
# import time

# def restart_ollama():
#     """Stops any running Ollama instance, sets environment variables, and restarts the server."""
#     print("Stopping any existing Ollama server...")
#     subprocess.run(["pkill", "-f", "ollama"], stderr=subprocess.DEVNULL)

#     # Set parallel threads for better CPU usage
#     os.environ["OLLAMA_NUM_PARALLEL"] = "8"  # Adjust as needed

#     print("Starting Ollama server with updated settings...")
#     subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

#     # Wait a few seconds to ensure the server starts
#     time.sleep(5)
#     print("Ollama server restarted successfully.")

# def main():
#     """Main function to run OCR processing after ensuring Ollama is ready."""
#     restart_ollama()

#     # Now run your Ollama-based OCR code
#       # Ensure you have this installed

#     ocr = OCRProcessor(model_name='granite3.2-vision')
#     result = ocr.process_image(
#         image_path="DataBase/Screenshot from 2025-03-08 22-32-42.png",  
#         format_type="text",  
#         language="eng"
#     )

#     print("OCR Result:\n", result)

# if __name__ == "__main__":
#     main()
