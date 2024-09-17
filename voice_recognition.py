import speech_recognition as sr 
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence 

r=sr.Recognizer() 
pathname = "voice.wav" 
output = "text.txt"
def add_style(text):
    style1 = ", no text"
    # style2 = "Monochrome, high contrast"
    # style3 = "black and white, lively, in motion"
    # style4 = "black and white, high contrast, rapid change, eerily"
    # style5 = "monochrome, lively, eerily, realistic"
    # final_text = text + "." + style1 + "\n" + text + "." + style2 + "\n" + text + "." + style3 + "\n" + text + "." + style4 + "\n" + text + "." +style5 + "\n" 
    final_text = text
    return final_text

def transcribe_audio_path(path): 
    with sr.AudioFile(path) as source:
        audio_listened = r.record(source) 
        text = r.recognize_google(audio_listened)
        text = add_style(text)
        f = open("text.txt", "w")
        f.write(text)
    return text

# def transcribe_audio_direct(file):
#     with sr.AudioFile(file) as source:
#         audio_listened = r.record(source)
#         text = r.recognize_google(audio_listened)
#         return text 
    
# if __name__ == "__main__":
#     text = transcribe_audio_path(pathname)
#     print(text)  