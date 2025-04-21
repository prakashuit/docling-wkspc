from pathlib import Path
from docling.document_converter import DocumentConverter
import json
import pandas as pd


converter = DocumentConverter()

# Define output folder path
output_dir = Path("C:/Prakash/source/docling-wkspc/output")

# source = "C:/Users/Administrator/Downloads/pdf-samples/wordpress-pdf-invoice-plugin-sample.pdf"
source = "C:/Users/Administrator/Downloads/pdf-samples/sample-invoice.pdf"
result = converter.convert(source)

print(result.document.export_to_markdown)

# Get the filename
doc_filename = result.input.file.stem
print(f"Document filename: {doc_filename}")

# Iterate over tables in the document and save them as CSV and HTML formats.
for table_idx, table in enumerate(result.document.tables):
  table_df: pd.DataFrame = table.export_to_dataframe()
  print(f"$$ Table {table_idx}")

  # Save as CSV
  table_df.to_csv(f"{doc_filename}-table-{table_idx}.csv")

  # Save as HTML
  html_filename = output_dir / f"{doc_filename}-table-{table_idx+1}.html"
  with html_filename.open("w") as fp:
    fp.write(table.export_to_html())