#pip install tabulate
#pip install pandas
import pandas as pd
xlFilePath=r'C:/Users/vivek/OneDrive/Desktop/College Project/modules/spreadSheetManipulation/xls_file.xlsx'
txtFilePath=r'C:/Users/vivek/OneDrive/Desktop/College Project/modules/spreadSheetManipulation/xlsToText.txt'
xlsFile = pd.ExcelFile(xlFilePath)
totalPages= xlsFile.sheet_names
with open(txtFilePath,'w') as textFile:
    for page in totalPages:
        dataFrame = xlsFile.parse(page)
        dataFrame=dataFrame.fillna(" ")#to replace NAN values with whitespace
        textFile.write("\nSheet name is:"+page+"\n")
        textFile.write(dataFrame.to_markdown())
    textFile.write('\n')

#df.to_markdown() for formated output
#to get only text use df.to_string()

