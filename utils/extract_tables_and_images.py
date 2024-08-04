import fitz  # PyMuPDF
from PIL import Image, ImageEnhance, ImageFilter
import io
import numpy as np
import cv2
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

import camelot
import pandas as pd
import glob
import os

def find_image_path(image_reference, images_info):
    for page_num, image_path in images_info:
        if image_reference in image_path:
            return image_path
    return None

def sort_images_numerically(image_list):
    # Function to extract the numerical part of the image name
    def extract_image_number(image_info):
        image_name = image_info[7]  # Assuming the image name is at the 7th position
        number = int(image_name[3:])  # Extract the numerical part after 'img'
        return number
    
    # Sort the image list based on the numerical part of the image names
    sorted_image_list = sorted(image_list, key=extract_image_number)
    
    return sorted_image_list

def generate_image_path(file_name, counter, ext):
    return f"{file_name}_img{counter:04d}.{ext}"

def extract_tables_and_images_from_pdfs(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    all_dfs = []
    
    for file in glob.glob(f"{input_folder}/*.pdf"):
        print(f"Reading File: {file}")
        # Extract tables using Camelot
        tables = camelot.read_pdf(file, pages='all', split_text=True)
        
        # Extract images using PyMuPDF
        pdf_document = fitz.open(file)
        images_info = []
        
        image_counter = 1  # Counter to keep track of image sequence

        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            image_list = page.get_images(full=True)

            # Sort the image list
            sorted_image_list = sort_images_numerically(image_list)
            
            for img_index, img in enumerate(sorted_image_list[2:]):
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                image_name = f"{os.path.basename(file).replace('.pdf', '')}_img{image_counter:04d}.{image_ext}"
                image_path = os.path.join(output_folder, image_name)
                with open(image_path, "wb") as img_file:
                    img_file.write(image_bytes)
                images_info.append((page_num + 1, image_path))
                image_counter += 1

        combined_df = pd.DataFrame()

        for page_num, table in enumerate(tables):
            df = table.df
            if page_num == 0:
                # Treat the first row of the first page as column headers
                df.columns = df.iloc[0]
                df = df[1:].reset_index(drop=True)
            else:
                # Ensure column names are consistent
                df.columns = combined_df.columns
            combined_df = pd.concat([combined_df, df], ignore_index=True)
        
        combined_df["Image Path"] = [image_path for _, image_path in images_info[:len(combined_df)]]
        images_info = images_info[len(combined_df):]  # Remove used image paths

        if file:
            output_csv_path = os.path.join(output_folder, f'{os.path.basename(file).replace(".pdf", "")}_combined_output.csv')
            combined_df.to_csv(output_csv_path, index=False)
            print(f"Table with Images Saved: {output_csv_path}")
        else:
            print("No tables found in the PDF files.")

# Example usage
if __name__ == "__main__":
    input_folder = '../resources/test_pdfs'
    output_folder = '../resources/test_csvs'
    extract_tables_and_images_from_pdfs(input_folder, output_folder)
