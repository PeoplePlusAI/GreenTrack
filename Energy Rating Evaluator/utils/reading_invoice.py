import pdfplumber
from utils.agent import call_agent
from PIL import Image
import pytesseract

class TextExtractor:
    def __init__(self, file_path=None, image=None):
        """
        Initialize with either a file path or a cv2 image object.
        """
        self.file_path = file_path
        self.image = image

    def extract_text_from_pdf(self):
        extracted_text = ""
        with pdfplumber.open(self.file_path) as pdf:
            for page in pdf.pages:
                extracted_text += page.extract_text() + "\n"
        return extracted_text

    def extract_text_from_image_file(self):
        image = Image.open(self.file_path)
        extracted_text = pytesseract.image_to_string(image)
        return extracted_text

    def extract_text_from_image(self):
        """
        Extract text from a cv2 image object.
        """
        if self.image is not None:
            extracted_text = pytesseract.image_to_string(self.image)
            return extracted_text
        else:
            raise ValueError("No image provided for text extraction.")

    def extract_text(self):
        """
        General method to extract text based on file type or image input.
        """
        if self.file_path:
            if self.file_path.lower().endswith(".pdf"):
                return self.extract_text_from_pdf()
            elif self.file_path.lower().endswith(
                ("jpg", "jpeg", "png", "bmp", "tiff", "webp")
            ):
                return self.extract_text_from_image_file()
            else:
                raise ValueError(
                    "Unsupported file type. Please use a PDF or image file."
                )
        elif self.image is not None:
            return self.extract_text_from_image()
        else:
            raise ValueError("No file path or image provided for text extraction.")

# Function to extract text from the invoice
def extract_text_from_invoice(invoice_content):
    features = [invoice_content]
    response = call_agent(features, f"list_names.txt")
    product_list = [item.strip() for item in response.split("\n") if item.strip()]
    return product_list

def process_invoice(image):
    # Create an instance of TextExtractor
    extractor = TextExtractor(image=image)
    # Extract text from the file
    extracted_text = extractor.extract_text()
    # Extract product names and model numbers
    product_dict = extract_text_from_invoice(extracted_text)
    return product_dict
