import pandas as pd
xlFilePath=r'C:/Users/vivek/OneDrive/Desktop/College Project/modules/spreadSheetManipulation/xls_file.xlsx'
csvFilePath=r'C:/Users/vivek/OneDrive/Desktop/College Project/modules/spreadSheetManipulation/XlsToCsv.csv'
sheetName=input("Enter the sheet name:")
try:
    read_file = pd.read_excel (xlFilePath,sheet_name=sheetName)
    read_file.to_csv (csvFilePath, index = None, header=True)
except ValueError as error:
    print(error)