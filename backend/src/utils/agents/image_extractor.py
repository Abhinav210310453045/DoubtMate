import fitz  # PyMuPDF
import pdfplumber
from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams, LTImage
import os
from PIL import Image
import io


class ImageDataExtract:
    def __init__(self, pdf_path, tool_name):
        self.pdf_path = pdf_path
        self.pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        self.tool_name = tool_name.lower()
        self.image_folder = f"{self.pdf_name}_images_{self.tool_name}"
        os.makedirs(self.image_folder, exist_ok=True)

    def _create_page_folder(self, page_num):
        """Create a folder for storing images from a specific page."""
        page_folder = os.path.join(self.image_folder, f"page_{page_num}")
        os.makedirs(page_folder, exist_ok=True)
        return page_folder

    def extract_images_pymupdf(self):
        """Extract images using PyMuPDF."""
        doc = fitz.open(self.pdf_path)

        for page_num, page in enumerate(doc, start=1):
            images = page.get_images(full=True)
            if images:
                page_folder = self._create_page_folder(page_num)

                for img_index, img in enumerate(images, start=1):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]

                    img_filename = f"page_{page_num}_img_{img_index}.{image_ext}"
                    img_path = os.path.join(page_folder, img_filename)

                    with open(img_path, "wb") as img_file:
                        img_file.write(image_bytes)

                    print(f"[PyMuPDF] Saved: {img_path}")

    # def extract_images_pdfplumber(self):
    #     """Extract images using pdfplumber."""
    #     with pdfplumber.open(self.pdf_path) as pdf:
    #         for page_num, page in enumerate(pdf.pages, start=1):
    #             images = page.images
    #             if images:
    #                 page_folder = self._create_page_folder(page_num)

    #                 for img_index, img in enumerate(images, start=1):
    #                     img_bytes = img["stream"].get_data()
    #                     img_ext = img["ext"]

    #                     img_filename = f"page_{page_num}_img_{img_index}.{img_ext}"
    #                     img_path = os.path.join(page_folder, img_filename)

    #                     with open(img_path, "wb") as img_file:
    #                         img_file.write(img_bytes)

    #                     print(f"[pdfplumber] Saved: {img_path}")

   

    def extract_images_pdfplumber(self):
        """Extract images using pdfplumber with proper format handling."""
        with pdfplumber.open(self.pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                images = page.images
                if images:
                    page_folder = self._create_page_folder(page_num)

                    for img_index, img in enumerate(images, start=1):
                        img_bytes = img["stream"].get_data()
                        
                        # Check for common formats (pdfplumber may not provide extension)
                        try:
                            image = Image.open(io.BytesIO(img_bytes))  # Try opening as an image
                            img_ext = image.format.lower()  # Auto-detect format (jpeg, png, etc.)
                        except Image.UnidentifiedImageError:
                            img_ext = "bin"  # Fallback for unknown formats

                        img_filename = f"page_{page_num}_img_{img_index}.{img_ext}"
                        img_path = os.path.join(page_folder, img_filename)

                        # Save properly detected images
                        if img_ext != "bin":
                            image.save(img_path, format=image.format)
                        else:
                            # Save as raw binary for debugging
                            with open(img_path, "wb") as img_file:
                                img_file.write(img_bytes)

                        print(f"[pdfplumber] Saved: {img_path}")



    def extract_images_pdfminer(self):
        """Extract images using PDFMiner."""
        for page_num, page_layout in enumerate(extract_pages(self.pdf_path, laparams=LAParams()), start=1):
            images_found = False

            for element in page_layout:
                if isinstance(element, LTImage):
                    images_found = True
                    page_folder = self._create_page_folder(page_num)

                    img_filename = f"page_{page_num}_img_1.png"
                    img_path = os.path.join(page_folder, img_filename)

                    with open(img_path, "wb") as img_file:
                        img_file.write(element.stream.get_data())

                    print(f"[PDFMiner] Saved: {img_path}")

            if not images_found:
                print(f"[PDFMiner] No images found on page {page_num}")

    def run(self):
        """Run the selected image extraction method based on the tool name."""
        if self.tool_name == "pymupdf":
            self.extract_images_pymupdf()
        elif self.tool_name == "pdfplumber":
            self.extract_images_pdfplumber()
        elif self.tool_name == "pdfminer":
            self.extract_images_pdfminer()
        else:
            print(f"Error: Unsupported tool '{self.tool_name}'. Choose from 'pymupdf', 'pdfplumber', 'pdfminer', or 'pdf2image'.")
            return

        print(f"\nImage extraction completed using {self.tool_name}.")

# Usage Example:
# pdf_extractor = ImageDataExtract("example.pdf", "pymupdf")
# pdf_extractor.run()

# pdf_extractor = DataExtract("example.pdf", "pdfplumber")
# pdf_extractor.run()


# from spire.pdf import *
# from spire.pdf.common import *
# import os

# class ImageDataExtract:
#     def __init__(self, pdf_path, tool_name="pymupdf"):
#         self.pdf_path = pdf_path
#         self.tool_name = tool_name
#         self.pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
#         self.image_folder = f"{self.pdf_name}_images_{self.tool_name}"
#         os.makedirs(self.image_folder, exist_ok=True)

#     def _create_page_folder(self, page_num):
#         """Create a folder for each page inside the main image folder."""
#         page_folder = os.path.join(self.image_folder, f"page_{page_num}")
#         os.makedirs(page_folder, exist_ok=True)
#         return page_folder

#     def extract_images_spirepdf(self):
#         """Extract images from PDF using Spire.PDF."""
#         # Load PDF
#         doc = PdfDocument()
#         doc.LoadFromFile(self.pdf_path)
#         imageHelper = PdfImageHelper()
#         index = 0

#         for i in range(doc.Pages.Count):
#             page = doc.Pages.get_Item(i)
#             imageInfos = imageHelper.GetImagesInfo(page)

#             if imageInfos:
#                 page_folder = self._create_page_folder(i + 1)  # Page-wise storage

#                 for img_index, imageInfo in enumerate(imageInfos, start=1):
#                     image = imageInfo.Image
#                     img_filename = f"page_{i+1}_img_{img_index}.png"
#                     img_path = os.path.join(page_folder, img_filename)

#                     # Save Image
#                     image.Save(img_path)
#                     print(f"[SpirePDF] Saved: {img_path}")

#         # Clean up
#         doc.Dispose()
