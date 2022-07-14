import moviepy.editor as mp
my_clip=mp.VideoFileClip(r"C:/Users/vivek/OneDrive/Desktop/College Project/modules/audiovideomanipulation/video_file.mp4")
my_clip.audio.write_audiofile("voice.mp3")
print("Converted")