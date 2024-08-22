def get_extraction_prompt(invoice_content):
    return f"""
    You are a helpful assistant who extracts product names and model numbers from invoices. 
    Your task is to extract only the product names from the given invoice. If a model number is present, 
    extract it as well and place it after the product name, separated by a tab. 
    Return only the product names and model numbers in this format: 'Product Name' or 'Product Name\tModel Number'.
    Do not include any other information. The output should be:
    'Gorilla Energy Saving 5 Star Rated 1200 mm Ceiling Fan With Remote Control And Bide Motor - Matt Brown\t8071Y7K862'
    
    Invoice:
    {invoice_content}
    """