#last updates : 06/08/2022,3pm
#pip install tabulate
from os import remove,path
#pip install pandas
from pandas import read_csv,read_excel,ExcelFile


"""
    this module has 4 function that can be used to convert:
    an excel file to text file
        xls_to_text(input_file:str,output_file:str)
            returns a dictionary return_data{'output':"",'error':"","output_file":""}
    a csv file to text file    
        csv_to_text(inputfile:str,output_file:str)
            returns a dictionary return_data{'output':"",'error':"","output_file":""}
    an excel file to csv file    
        xls_to_csv(input_file:str,output_file:str,sheet_name:str)
            returns a dictionary return_data{'output':"",'error':"","output_file":""}
    finds a given column of data    
        search_columns(input_file:str,output_file:str,sheet_name:str,column_name:str)
            returns a dictionary return_data{'output':"",'error':"","output_file":""}
"""
#note:
#df.to_markdown() for formated output
#df.to_string()for only text output

#custom error
class CustomError(Exception):
    error_data=""

#function that returns file format
def file_type(input_file:str):    
    file_extension=path.splitext(input_file)
    return(file_extension[1].lower())

#function that returns the size of the file in MB
def filesize(input_file:str):
    return (path.getsize(input_file)/1048576)

#------function 1----------
def xls_to_text(input_file:str,output_file:str):
    """
    this function converts an excel file to text file
    """
    #dictionary to store output 
    return_data={
        "output":"",
        "error":"",
        "output_file":""
    }
    try:
        #checking for correct file format
        input_file_types=[".xlsx",".xls"]
        output_file_types=[".txt"]
        input_file_type=file_type(input_file)
        if input_file_type not in input_file_types:
            CustomError.error_data="Given file format ("+input_file_type+") is not supported..!"
            raise CustomError
        output_file_type=file_type(output_file)
        if output_file_type not in output_file_types:
            CustomError.error_data="Given file format ("+output_file_type+") is not supported..!"
            raise CustomError

        #cheking if the file is too big
        max_size=10#confirm the max size
        if(filesize(input_file)>max_size):
            CustomError.error_data="Maximum file size is "+str(max_size)+"MB."
            raise CustomError

        #checking if the file is empty
        df=read_excel(input_file)
        if df.empty:
            CustomError.error_data="file is empty"
            raise CustomError

        #excel file variable is created
        xlsFile = ExcelFile(input_file)
        #sheet name in the excel file
        sheet_name= xlsFile.sheet_names
        #opening textfile to write data
        with open(output_file,'w') as textFile:
            #looping through pages 
            for page in sheet_name:
                #storing data in each frame in a datafram 
                dataFrame = xlsFile.parse(page)
                #removing null values in the dataframe
                dataFrame=dataFrame.fillna(" ")#to replace NAN values with whitespace
                #printing sheet name on the textfile
                textFile.write("\nSheet name is:"+page+"\n")
                #printing data on the text file
                textFile.write(dataFrame.to_string())
                #adding new line after each page
                textFile.write('\n')
        #storing output in dictionary
        return_data['output']="done"
        return_data['output_file']=output_file #path of saved file
    except CustomError:
        #writing error data
        return_data["error"]=CustomError.error_data
        #removing output file if an error occurs
        remove(output_file)
    except Exception as e:
        #removing output file if an error occurs
        remove(output_file)
        #writing error
        return_data['error']=e  
    return return_data   


#------function 2----------
def csv_to_text(input_file:str,output_file:str):
    """
    This function converts csv file to Text file
    """
    #dictionary to store output 
    return_data={
        "output":"",
        "error":"",
        "output_file":""
    }
    try:
        #checking for correct file format
        input_file_types=[".csv"]
        output_file_types=[".txt"]
        input_file_type=file_type(input_file)
        if input_file_type not in input_file_types:
            CustomError.error_data="Given file format ("+input_file_type+") is not supported..!"
            raise CustomError
        output_file_type=file_type(output_file)
        if output_file_type not in output_file_types:
            CustomError.error_data="Given file format ("+output_file_type+") is not supported..!"
            raise CustomError
        #cheking if the file is too big
        max_size=10#confirm the max size
        if(filesize(input_file)>max_size):
            CustomError.error_data="Maximum file size is "+str(max_size)+"MB."
            raise CustomError

        #checking if the file is empty
        df=read_csv(input_file)
        if df.empty:
            CustomError.error_data="file is empty"
            raise CustomError

        #reading the data from cvs file to a dataframe
        dataFrame=read_csv(input_file)
        #opening text file to write
        with open(output_file,'w') as textFile:
            #replacing null values in dataframe with whitespace
            dataFrame=dataFrame.fillna(" ")
            #writing data from dataframe to a textfile
            textFile.write(dataFrame.to_string())
            textFile.write('\n')
        #storing output in dictionary
        return_data['output']="done"
        return_data['output_file']=output_file #path of saved file
    except CustomError:
        #EmptyDataError() is same as file is empty
        #writing error data
        return_data["error"]=CustomError.error_data
        #removing output file if an error occurs
        remove(output_file)
    except Exception as e:
        #removing output file if an error occurs
        remove(output_file)
        #writing error
        return_data['error']=e
          
    return return_data   


#------function 3----------
def xls_to_csv(input_file:str,output_file:str,sheet_name:str):
    """
    This function converts and Excel file to Csv  file
    """
    #dictionary to store output 
    return_data={
        "output":"",
        "error":"",
        "output_file":""
    }
    try:
        #checking for correct file format
        input_file_types=[".xlsx",".xls"]
        output_file_types=[".csv"]
        input_file_type=file_type(input_file)
        if input_file_type not in input_file_types:
            CustomError.error_data="Given file format ("+input_file_type+") is not supported..!"
            raise CustomError
        output_file_type=file_type(output_file)
        if output_file_type not in output_file_types:
            CustomError.error_data="Given file format ("+output_file_type+") is not supported..!"
            raise CustomError

        #cheking if the file is too big
        max_size=10#confirm the max size
        if(filesize(input_file)>max_size):
            CustomError.error_data="Maximum file size is "+str(max_size)+"MB."
            raise CustomError

        #checking if the file is empty
        df=read_excel(input_file)
        if df.empty:
            CustomError.error_data="file is empty"
            raise CustomError

        #reading the data a given sheet of excel file to a dataframe
        read_file = read_excel (input_file,sheet_name=sheet_name)
        #writing the dataframe onto a csv file
        #header specifies the column name in the sheet
        read_file.to_csv (output_file, index = None, header=True)
        #storing output in dictionary
        return_data['output']="done"
        return_data['output_file']=output_file #path of saved file
    
    except CustomError:
        #writing error data
        return_data["error"]=CustomError.error_data
        #removing output file if an error occurs
        remove(output_file)
    except ValueError:
        #removing output file if an error occurs
        remove(output_file)
        #error generated when sheet name is not found
        return_data["error"]="Sheet not found..!"
    except Exception as e:
        #removing output file if an error occurs
        remove(output_file)
        #writing error
        return_data['error']=e  
    return return_data   

#------function 4----------
def search_columns(input_file:str,output_file:str,sheet_name:str,column_name:str):
    """
    this function is used to find specified column(s) in an excel file
    """
    #dictionary to store output 
    return_data={
        "output":"",
        "error":"",
        "output_file":""
    }
    try:
        #checking for correct file format
        input_file_types=[".xlsx",".xls"]
        output_file_types=[".txt"]
        input_file_type=file_type(input_file)
        if input_file_type not in input_file_types:
            CustomError.error_data="Given file format ("+input_file_type+") is not supported..!"
            raise CustomError
        output_file_type=file_type(output_file)
        if output_file_type not in output_file_types:
            CustomError.error_data="Given file format ("+output_file_type+") is not supported..!"
            raise CustomError

        #cheking if the file is too big
        max_size=10#confirm the max size
        if(filesize(input_file)>max_size):
            CustomError.error_data="Maximum file size is "+str(max_size)+"MB."
            raise CustomError
            
        #checking if the file is empty
        df=read_excel(input_file)
        if df.empty:
            CustomError.error_data="file is empty"
            raise CustomError

        #excel file variable is created
        xlsFile = ExcelFile(input_file)
        #all the sheet names in the excel file
        sheetNames= xlsFile.sheet_names
        #cheking if given sheetname is available or not
        if(sheet_name in sheetNames):
            #open text file to write
            with open(output_file,'w') as textFile:
                #creating dataframe of the given xl sheet
                dataFrame = xlsFile.parse(sheet_name)
                #finding total rows and columns in the sheet
                dimension=dataFrame.shape  #returns rows and columns as tuple
                #creating a list if the user gives more than 1 column
                column_name=column_name.split(",",dimension[1])
                #column_name=input("Enter the column name(s):").split(",",dimension[1])
                #replacing null with space
                dataFrame=dataFrame.fillna(" ")
                #writing sheet name on txt file
                textFile.write("Sheet name is:"+sheet_name+"\n")
                #writing data on the txt file
                textFile.write(dataFrame[column_name].to_string())
                textFile.write("\n") 
        else:
            #returning error no sheet found
             raise ValueError
        #storing output in dictionary
        return_data['output']="done"
        return_data['output_file']=output_file #path of saved file
   
    except CustomError:
        #writing error data
        return_data["error"]=CustomError.error_data
        #removing output file if an error occurs
        remove(output_file)
    except ValueError:
        #writing error data
        return_data["error"]="Sheet not found..!"
        #removing output file if an error occurs
        remove(output_file)
    except KeyError:
        #keyerror means no columns
        #removing output file if an error occurs
        remove(output_file)
        #returning error if no data found
        return_data['error']="no column found..!"
    except Exception as e:
        #removing output file if an error occurs
        remove(output_file)
        #writing error
        return_data['error']=e
    return return_data 