from google_voice import GoogleVoice
from playsound import playsound

synthesizer = GoogleVoice()
"""
synthesizer.text_to_speech("Okay ... starting the guidance system. Remember, the left vibrator indicates a rotation to the left, and the right vibrator indicates a rotation to the right. The guidance system gives you a suggested angle of rotation to turn to in order to avoid obstacles. A vibrator motor will continuously vibrate until you have rotated towards the suggested angle. With all that out of the way, let us begin!", "guide")
playsound("guide.wav")

synthesizer.text_to_speech("Okay ... hold on a moment ... I will now scan the scene for any recognizable objects", "describe")
playsound("describe.wav")

synthesizer.text_to_speech("Just a moment ... I need to first read what the text says", "read")
playsound("read.wav")
"""

synthesizer.text_to_speech("Hello, My name is VICS. How can I be of assistance to you today.", "greet")
playsound("greet.wav")
