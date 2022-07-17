# Python program to convert text file to PDF using FPDF
#requirement
"""a single line in a text file should not exceed the size of an A4 sheet"""
from fpdf import FPDF #pip install fpdf
def text_to_pdf(input_file:str,output_file:str):
    """
        takes a text file as input and converts it into a pdf file 
        Note:
            a single line in a text file should not exceed the size of an A4 sheet
    """
    #dictionary to store output 
    return_data={
        "output":"",
        "error":"",
        "output_file":""
    }
    try:
        #variable of pdf object 
        pdf = FPDF() 
        #adding page to the variable
        pdf.add_page() 
        #setting font
        pdf.set_font("Arial", size = 15) 

        #opening text file for conversion 
        with open(input_file, "r",encoding='utf-8') as text_file:
            for data in text_file:
                pdf.cell(w=250, h=10, txt = data, ln =1 , align = 'L') 
            pdf.output(output_file)
        #storing output in dictionary
        return_data['output']="done"
        return_data['output_file']=output_file #path of saved file
    except Exception as e:
        #writing error
        return_data['error']=e  
    return return_data   
