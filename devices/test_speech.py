from google_voice import GoogleVoice
from playsound import playsound

synthesizer = GoogleVoice()
synthesizer.list_languages()
synthesizer.list_voices("en")
synthesizer.text_to_speech(input("Voice style: "), input("Type in speech"), "response")
playsound("response.wav")
