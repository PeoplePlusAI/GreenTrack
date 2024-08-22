import os
import re

import pdfplumber
import pytesseract
from groq import Groq
from PIL import Image

from prompt import get_extraction_prompt

# Replace with your actual Groq API key
GROQ_API_KEY = "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"

# Initialize the Groq client
client = Groq(api_key=GROQ_API_KEY)


class TextExtractor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_type = self._detect_file_type()

    def _detect_file_type(self):
        return self.file_path.split(".")[-1].lower()

    def extract_text_from_pdf(self):
        extracted_text = ""
        with pdfplumber.open(self.file_path) as pdf:
            for page in pdf.pages:
                extracted_text += page.extract_text() + "\n"
        return extracted_text

    def extract_text_from_image(self):
        image = Image.open(self.file_path)
        extracted_text = pytesseract.image_to_string(image)
        return extracted_text

    def extract_text(self):
        if self.file_type == "pdf":
            return self.extract_text_from_pdf()
        elif self.file_type in ["jpg", "jpeg", "png", "bmp", "tiff", "webp"]:
            return self.extract_text_from_image()
        else:
            raise ValueError("Unsupported file type. Please use a PDF or image file.")


# Function to extract text from the invoice
def extract_text_from_invoice(invoice_content):
    prompt = get_extraction_prompt(invoice_content)
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-70b-8192",
    )

    response = chat_completion.choices[0].message.content.split("\n")[1:]
    product_dict = {
        parts[0].strip(): (parts[1].strip() if len(parts) > 1 else None)
        for string in response
        if (parts := string.split("\t"))
    }
    product_dict = {k: v for k, v in product_dict.items() if k}
    return product_dict


def process_invoice(file_path):
    # Create an instance of TextExtractor
    extractor = TextExtractor(file_path)

    # Extract text from the file
    extracted_text = extractor.extract_text()

    # Extract product names and model numbers
    product_dict = extract_text_from_invoice(extracted_text)
    print("Product Dictionary:")
    print(product_dict)

    return product_dict


# Example usage
# file_path = '../invoice/invoice5.png'  # or 'path/to/your/file.pdf'
# product_dict = process_invoice(file_path)
