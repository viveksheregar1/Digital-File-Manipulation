import fitz #PyMuPDF

with fitz.open(r"C:/Users/vivek/OneDrive/Desktop/College Project/modules/file manipulation/pdf_file.pdf") as doc:
    text = ""
    for page in doc:
        text += page.get_text()
with open(r"C:/Users/vivek/OneDrive/Desktop/College Project/modules/file manipulation/pdf_to_text.txt",'w', encoding="utf-8") as text_file:
    text_file.write((text))
