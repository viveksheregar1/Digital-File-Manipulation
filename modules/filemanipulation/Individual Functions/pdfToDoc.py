from pdf2docx import parse
from typing import Tuple
input_file=r"C:/Users/vivek/OneDrive/Desktop/College Project/modules/file manipulation/pdf_file.pdf"
output_file=r"C:/Users/vivek/OneDrive/Desktop/College Project/modules/file manipulation/Doc.docx"
pages=()
#Converts pdf to docx
if pages:
    pages = [int(i) for i in list(pages) if i.isnumeric()]
result = parse(input_file,output_file, pages=pages)