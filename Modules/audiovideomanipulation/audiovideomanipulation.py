from io import TextIOWrapper
import moviepy.editor as mp #pip install moviepy
import speech_recognition as sr #pip install speechrecognition
import filetype #pip install filetype
import os
from os import path
from pydub import AudioSegment
"""
this package consists of 3 functions:
video_to_text(input_file:str,output_file:str)
    returns a dictionary return_data{'output':"",'error':"","output_file":""}
audio_to_text(input_file:str,output_file:str)
    returns a dictionary return_data{'output':"",'error':"","output_file":""}
video_to_audio(input_file:str,output_file:str)
    returns a dictionary return_data{'output':"",'error':"","output_file":""}
"""

#function to find file type
def file_type(input_file:str):
    #r"C:/Users/vivek/OneDrive/Desktop/College Project/modules/audiovideomanipulation/audio_file.wav"    
    file_type = filetype.guess(input_file)
    return file_type.extension
#os.remove("file name")

def convert(input_file:str):
    #return converted file path
    #input_file = r"C:/Users/vivek/OneDrive/Desktop/College Project/modules/audiovideomanipulation/IndividualFunction/voice.mp3"
    output_file="mp3_temp_audio.wav"
    # convert wav to mp3                                                            
    sound = AudioSegment.from_mp3(input_file)
    sound.export(output_file,format="wav")
    return output_file

#------function 1----------
def video_to_text(input_file:str,output_file:str):
    """
        takes a video as an input and extracts the words spoken in the video using
        recognize_google() api.
    """
    #dictionary to store output 
    return_data={
        "output":"",
        "error":"",
        "output_file":""
    }
    try:
        #input_file=r"C:/Users/vivek/OneDrive/Desktop/College Project/modules/audiovideomanipulation/video_file.mp4"
        #output_file=r"C:/Users/vivek/OneDrive/Desktop/College Project/modules/audiovideomanipulation/video_to_text.txt"
        #storing videoclip in my_clip
        my_clip=mp.VideoFileClip(input_file)
        #writing audio from video to a audio for furthur use 
        my_clip.audio.write_audiofile("temp_audio.wav")
        #audio file name is audio_file.wav and it's path is stored in sound variable
        sound="temp_audio.wav"
        #recognizer object
        r = sr.Recognizer()
        #opening audio file
        with sr.AudioFile(sound) as source:
            #adjusting the audio file for extraction
            r.adjust_for_ambient_noise(source)
            audio=r.listen(source)
            #converting audio to text using google api
            text=r.recognize_google(audio)
            #print("converted to text and saved in a file and the text is:\n"+ text)
            with open(output_file,'w') as audio_to_text_file:
                #writing audio on the text file
                audio_to_text_file.write(text)
        #storing output in dictionary
        return_data['output']="done"
        return_data['output_file']=output_file #path of saved file
    except Exception as e:
        #writing error
        return_data['error']=e  
    #remove the temporarily created audio file
    os.remove("temp_audio.wav")
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
        #input_file=r"C:/Users/vivek/OneDrive/Desktop/College Project/modules/audiovideomanipulation/video_file.mp4"
        #output_file=r"C:/Users/vivek/OneDrive/Desktop/College Project/modules/audiovideomanipulation/video_to_audio.wav"
        #storing videoclip in my_clip
        my_clip=mp.VideoFileClip(input_file)
        #writing audio extracted from video to a .wav file 
        my_clip.audio.write_audiofile(output_file)
        return_data['output']="done"
        return_data['output_file']=output_file #path of saved file
    except Exception as e:
        return_data['error']=e     
    return return_data 


#------function 3----------
def audio_to_text(input_file:str,output_file:str):
    """
        takes a audio as an input and extracts the words spoken in the audio using
        recognize_google() api.
    """
    return_data={
        "output":"",
        "error":"",
        "output_file":""
    }
    try:
        input_file = r"C:/Users/vivek/OneDrive/Desktop/College Project/modules/audiovideomanipulation/audio.mp3"
        #input_file=r"C:/Users/vivek/OneDrive/Desktop/College Project/modules/audiovideomanipulation/audio_file.wav"
        output_file=r"C:/Users/vivek/OneDrive/Desktop/College Project/modules/audiovideomanipulation/audio_to_text.txt"
        #recognizer object
        r = sr.Recognizer()
        #convert mp3 format to wav
        isconverted=False
        if(file_type(input_file)!="wav"):
            isconverted=True
            input_file=convert(input_file)

        with sr.AudioFile(input_file) as source:
            #filtering the audio to cleanit
            r.adjust_for_ambient_noise(source)
            audio=r.listen(source)
            #text file stores the text from audio file converted by api
            text=r.recognize_google(audio)
            #print("converted to text and saved in a file and the text is:\n"+ text)
            #storing data in text file
            with open(output_file,'w') as audio_to_text_file:
                audio_to_text_file.write(text)
        #writing output
        print(input_file)
        return_data['output']="done"
        return_data['output_file']=output_file #path of saved file
    except Exception as e:
        return_data['error']=e   
    if(isconverted):
        os.remove("mp3_temp_audio.wav")
    return return_data 

print(audio_to_text("data",'data'))