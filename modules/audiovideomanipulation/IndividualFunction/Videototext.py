import moviepy.editor as mp
import speech_recognition as sr

my_clip=mp.VideoFileClip(r"C:\Users\vivek\OneDrive\Desktop\College Project\modules\video audio manipulation\samplevideo.mp4")
my_clip.audio.write_audiofile("sampleaudio.wav")
sound="sampleaudio.wav"
r = sr.Recognizer()
with sr.AudioFile(sound) as source:
    r.adjust_for_ambient_noise(source)
    print("converting")
    audio=r.listen(source)
    try:
        text=r.recognize_google(audio)
        print("converted to text and saved in a file and the text is:\n"+ text)
        audio_to_text_file=open(r'C:\Users\vivek\OneDrive\Desktop\College Project\modules\video audio manipulation\video_to_text.txt','w')
        audio_to_text_file.write(text)
        audio_to_text_file.close()
    except Exception as e:
        print(e)