import speech_recognition as sr
sound=r"C:/Users/vivek/OneDrive/Desktop/College Project/modules/audiovideomanipulation/audio_file.wav"
r = sr.Recognizer()
with sr.AudioFile(sound) as source:
    r.adjust_for_ambient_noise(source)
    print("converting")
    audio=r.listen(source)
    try:
        print("converted"+r.recognize_google(audio))
    except Exception as e:
        print(e)



