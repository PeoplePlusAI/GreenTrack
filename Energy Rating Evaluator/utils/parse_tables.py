import camelot
import pandas as pd
import glob

for file in glob.glob("../resources/pdfs/*.pdf"):
    print(f"Reading File: {file}")
    tables = camelot.read_pdf(file, pages='all', split_text=True)
    all_dfs = []
    for table in tables:
        all_dfs.append(table.df)
    combined_df = pd.concat(all_dfs, ignore_index=True)
    output_path = file.replace("/pdfs/", "/csvs/").replace(".pdf",".csv")
    combined_df.to_csv(output_path, index=False)
    print(f"Table Saved: {output_path}")
