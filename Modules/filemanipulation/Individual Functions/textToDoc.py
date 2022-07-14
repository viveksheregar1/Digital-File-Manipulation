#importing docx
import docx
#opening txt file

with open(r"C:/Users/vivek/OneDrive/Desktop/College Project/modules/file manipulation/txt_file.txt") as text_file:
    #reading lines in the docx file as list
    lines=text_file.readlines()
    #document object
    document_file=docx.Document()
    for data in lines:
        #writing text on docx file
        document_file.add_paragraph(data)
        document_file.save(r"C:/Users/vivek/OneDrive/Desktop/College Project/modules/file manipulation/text_to_doc.docx") 