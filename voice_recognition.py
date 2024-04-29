import speech_recognition as sr 
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence 

r=sr.Recognizer() 
pathname = "voice.wav" 
output = "text.txt"

def transcribe_audio_path(path): 
    with sr.AudioFile(path) as source:
        audio_listened = r.record(source) 
        text = r.recognize_google(audio_listened)
        f = open("text.txt", "w")
        f.write(text)
    return text

# def transcribe_audio_direct(file):
#     with sr.AudioFile(file) as source:
#         audio_listened = r.record(source)
#         text = r.recognize_google(audio_listened)
#         return text 
    
if __name__ == "__main__":
    text = transcribe_audio_path(pathname)
    print(text)  