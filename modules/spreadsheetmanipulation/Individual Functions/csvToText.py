import pandas as pd
csvFilePath=r'C:/Users/vivek/OneDrive/Desktop/College Project/modules/spreadSheetManipulation/csv_file.csv'
txtFilePath=r'C:/Users/vivek/OneDrive/Desktop/College Project/modules/spreadSheetManipulation/CsvToText.txt'
dataFrame=pd.read_csv(csvFilePath)
with open(txtFilePath,'w') as textFile:
    dataFrame=dataFrame.fillna(" ")#to replace NAN values with whitespace
    textFile.write(dataFrame.to_markdown())
    textFile.write('\n')


