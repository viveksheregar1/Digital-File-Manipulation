import pandas as pd
xlFilePath=r'C:/Users/vivek/OneDrive/Desktop/College Project/modules/spreadSheetManipulation/xls_file.xlsx'
txtFilePath=r'C:/Users/vivek/OneDrive/Desktop/College Project/modules/spreadSheetManipulation/searchColumn.txt'
xlsFile = pd.ExcelFile(xlFilePath)
sheetNames= xlsFile.sheet_names
print(sheetNames)
sheet=input("Enter the sheet name:")
if(sheet in sheetNames):
    with open(txtFilePath,'w') as textFile:
        dataFrame = xlsFile.parse(sheet)
        dimension=dataFrame.shape#total rows and columns as tuple
        try:
            column=input("Enter the column name(s):").split(",",dimension[1])
            #print(dataFrame[column].to_markdown())
            dataFrame=dataFrame.fillna(" ")
            textFile.write("Sheet name is:"+sheet+"\n")
            textFile.write(dataFrame[column].to_markdown())
            textFile.write("\n")
        except KeyError:
            print("no column found")
else:
    print("no sheet found")