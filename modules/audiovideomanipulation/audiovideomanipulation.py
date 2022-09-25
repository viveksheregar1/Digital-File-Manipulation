#last updates : 23/08/2022,5pm
from moviepy.editor import VideoFileClip #pip install moviepy (this uses ffmpeg underneath)
from os import path,remove,stat
from pydub import AudioSegment #pip install pydub
from gtts import gTTS #pip install gtts

"""
this package consists of 3 functions:
text_to_audio(input_file:str,output_file:str)
    returns a dictionary return_data{'output':"",'error':"","output_file":""}
trim_audio(input_file:str,output_file:str,startmin:int,startsec:int,endmin:int,endsec:int)
    returns a dictionary return_data{'output':"",'error':"","output_file":""}
video_to_audio(input_file:str,output_file:str)
    returns a dictionary return_data{'output':"",'error':"","output_file":""}
"""

#custom exception
class CustomError(Exception):
    error_data=""

#function to find file type
def file_type(input_file:str):    
    file_extension=path.splitext(input_file)
    return(file_extension[1].lower())

#function that returns the size of the file in MB
def filesize(input_file:str):
    return (path.getsize(input_file)/1048576)

#------function 1----------
def text_to_audio(input_file:str,output_file:str):
    """
        takes a text file as an input and converts it into audio
    """
    return_data={
        "output":"",
        "error":"",
        "output_file":""
    }
    try:
        #checking for correct file format
        input_file_types=[".txt"]
        output_file_types=[".wav",".mp3",".aiff",".aac",".ogg","wma",".flac",".alac"]
        input_file_type=file_type(input_file)
        if input_file_type not in input_file_types:
            CustomError.error_data="Given file format ("+input_file_type+") is not supported..!"
            raise CustomError
        output_file_type=file_type(output_file)
        if output_file_type not in output_file_types:
            CustomError.error_data="Given file format ("+output_file_type+") is not supported..!"
            raise CustomError

        #cheking if the file is too big
        max_size=1#confirm the max size
        if(filesize(input_file)>max_size):
            CustomError.error_data="Maximum file size is "+str(max_size)+"MB."
            raise CustomError

        #cheking if the file is empty
        if stat(input_file).st_size == 0:
            CustomError.error_data="file is empty"
            raise CustomError
        
        mytext=""
        with open(input_file,"r")as file:
            mytext=file.read()
        myobj = gTTS(text=mytext, lang="en", slow=False)
        myobj.save(output_file)
        return_data['output']="done"
        return_data['output_file']=output_file #path of saved file
    except CustomError:
        #removing  previously created output file
        remove(output_file)
        #writing error
        return_data["error"]=CustomError.error_data
    except Exception as e:
        #writing error
        return_data['error']=e 
        #removing  previously created output file
        remove(output_file)    
    return return_data 

#------function 2----------
def video_to_audio(input_file:str,output_file:str):
    """
        takes a video as an input and extracts the audio from the video
    """
    return_data={
        "output":"",
        "error":"",
        "output_file":""
    }
    try:
        #checking for correct file format
        input_file_types=[".mp4",".mkv",".mov",".avi",".mpeg",".webm",".wmv",".flv",".ogg",".3gp",".avchd",".m4v"]
        output_file_types=[".wav",".mp3",".aiff",".aac",".ogg","wma",".flac",".alac"]
        input_file_type=file_type(input_file)
        if input_file_type not in input_file_types:
            CustomError.error_data="Given file format ("+input_file_type+") is not supported..!"
            raise CustomError
        output_file_type=file_type(output_file)
        if output_file_type not in output_file_types:
            CustomError.error_data="Given file format ("+output_file_type+") is not supported..!"
            raise CustomError

        #cheking if the file is too big
        max_size=100#confirm the max size
        if(filesize(input_file)>max_size):
            CustomError.error_data="Maximum file size is "+str(max_size)+"MB."
            raise CustomError

        #checking if file is empty
        if(stat(input_file).st_size == 0):
            CustomError.error_data="file is empty..!"
            raise CustomError

        #storing videoclip in my_clip
        my_clip=VideoFileClip(input_file)
        #writing audio extracted from video to a .wav file 
        my_clip.audio.write_audiofile(output_file)
        return_data['output']="done"
        return_data['output_file']=output_file #path of saved file
    except CustomError:
        #removing  previously created output file
        remove(output_file)
        #writing error
        return_data["error"]=CustomError.error_data
    except AttributeError:
        #removing  previously created output file
        remove(output_file)
        #writing error
        return_data['error']="video has no audio"
    except Exception as e:
        #writing error
        return_data['error']=e 
        #removing  previously created output file
        remove(output_file)    
    return return_data 


#------function 3----------
def trim_audio(input_file:str,output_file:str,startmin:int,startsec:int,endmin:int,endsec:int):
    """
        takes a audio file,start and end time as input and crops the audio to specifies time
    """
    return_data={
        "output":"",
        "error":"",
        "output_file":""
    }
    try:
        #checking for correct file format
        input_file_types=[".wav",".mp3",".ogg",".flv",".raw"]
        output_file_types=[".wav",".mp3",".aiff",".aac",".ogg","wma",".flac",".alac"]
        input_file_type=file_type(input_file)
        if input_file_type not in input_file_types:
            CustomError.error_data="Given file format ("+input_file_type+") is not supported..!"
            raise CustomError
        output_file_type=file_type(output_file)
        if output_file_type not in output_file_types:
            CustomError.error_data="Given file format ("+output_file_type+") is not supported..!"
            raise CustomError

        #cheking if the file is too big
        max_size=20#confirm the max size
        if(filesize(input_file)>max_size):
            CustomError.error_data="Maximum file size is "+str(max_size)+"MB."
            raise CustomError
            
        #checking if file is empty
        if(stat(input_file).st_size == 0):
            CustomError.error_data="file is empty..!"
            raise CustomError
        
        if(input_file_type==".mp3"):
            sound=AudioSegment.from_mp3(input_file)
        elif(input_file_type==".flv"):
            sound=AudioSegment.from_flv(input_file)
        elif(input_file_type==".ogg"):
            sound=AudioSegment.from_ogg(input_file)
        elif(input_file_type==".raw"):
            sound=AudioSegment.from_raw(input_file)
        elif(input_file_type==".wav"):
            sound=AudioSegment.from_wav(input_file)
        
        duration=sound.duration_seconds
        # Time to milliseconds conversion
        StrtTime = startmin*60*1000+startsec*1000
        EndTime = endmin*60*1000+endsec*1000
        if(StrtTime>(duration*1000)):
            CustomError.error_data="Start time must be less than audio length"
            raise CustomError
        if(StrtTime>EndTime):
            CustomError.error_data="End time must be greater than Start time"
            raise CustomError
        # Opening file and extracting portion of it
        extract = sound[StrtTime:EndTime]
        a,output_format=output_file_type.split(".")
        # Saving file in required location
        extract.export(output_file, format=output_format)
        return_data['output']="done"
        return_data['output_file']=output_file #path of saved file

    except CustomError:
        #removing  previously created output file
        remove(output_file)
        #writing error
        return_data["error"]=CustomError.error_data
    except Exception as e:
        #writing error
        return_data['error']=e 
        #removing  previously created output file
        remove(output_file)    
    return return_data 
