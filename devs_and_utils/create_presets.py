from google_voice import GoogleVoice
from playsound import playsound

synthesizer = GoogleVoice()
<<<<<<< HEAD

=======
>>>>>>> e2991caa0b3fcdd856661b2f5a8d4e9b7cefdd31
"""
synthesizer.text_to_speech("Okay ... starting the guidance system. Remember, the left vibrator indicates a rotation to the left, and the right vibrator indicates a rotation to the right. The guidance system gives you a suggested angle of rotation to turn to in order to avoid obstacles. A vibrator motor will continuously vibrate until you have rotated towards the suggested angle. With all that out of the way, let us begin!", "guide")
playsound("guide.wav")

synthesizer.text_to_speech("Okay ... hold on a moment ... I will now scan the scene for any recognizable objects", "describe")
playsound("describe.wav")

synthesizer.text_to_speech("Just a moment ... I need to first read what the text says", "read")
playsound("read.wav")
"""

<<<<<<< HEAD
synthesizer.text_to_speech("sheeeeeeeeeeeeeeesh", "s1.wav")
playsound("s1.wav")
synthesizer.text_to_speech("There is a person in directly in front of you and a chair to your left", "response")
playsound("response.wav")
=======
synthesizer.text_to_speech("There  is a person directly in front of you ... and there is a chair to your left", "fake")
playsound("fake.wav")
>>>>>>> e2991caa0b3fcdd856661b2f5a8d4e9b7cefdd31
