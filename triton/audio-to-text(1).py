import speech_recognition as sr

def convert_audio_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Sorry, could not understand the audio."
        except sr.RequestError as e:
            return f"Could not request results; {e}"

def save_text_to_file(text, output_file):
    text = "painting of " + text
    with open(output_file, "w") as file:
        file.write(text)

if __name__ == "__main__":
    print("audio to text start running")
    audio_file = "./recordedAudio/sample-audio.wav"  # Change this to your audio file path
    output_file = "./outputText/output.txt"  # Change this to your desired output file path
    text = convert_audio_to_text(audio_file)
    save_text_to_file(text, output_file)
    print("Conversion complete. Text saved to", output_file)
