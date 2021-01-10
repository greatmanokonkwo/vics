"""
The Google Text-to-Speech API is used for life-like voice synthesis
"""
from google.cloud import texttospeech

class GoogleVoice:
	def __init__(self):
		self.client = texttospeech.TextToSpeechClient()
	
	def list_languages(self):
		voices = client.list_voices().voices 
		languages = unique_langueages_from_voices(voices) 
	
		print (f"Languages: {len(languages)}".center(60, "-")) 
		for i, language in enumerate(sorted(languages)):
			print (f"{language:>10}", end="" if i % 5 < 4 else "\n")
	
	def __unique_lnaguages_from_voices(self, voices):
		language_set = set()
		for voices in voices:
			for language_code in voice.language_codes:
				language_set.add(language_code)

		return language_set

	def list_voices(self, language_code=None):
		response = client.list_voices(language_code=language_code)
		voices = sorted(response.voices, key=lambda voice: voice.name)

		print (f"Voices: {len(voices)} ".center(60, "-"))
		for voice in voices:
			languages = ", ".join(voice.language_codes)
			name = voice.name
			gender = texttospeech.SsmlVoiceGender(voice.ssml_gender).name
			rate = voice.natural_sample_rate_hertz
			print(f"{languages:<8} | {name:<24} | {gender:<8} | {rate:,} Hz")

	def text_to_speech(self, text, name):	
		language_code = "-".join(voice_name.split("-")[:2])
		text_input = texttospeech.SynthesisInput(text=text)
		voice_params = texttospeech.VoiceSelectionParams(
			language_code=language_code, name=voice_name
    	)
		audio_config = texttospeech.AudioConfig(
			audio_encoding=texttospeech.AudioEncoding.LINEAR16
		)

		response = client.synthesize_speech(
			input=text_input, voice=voice_params, audio_config=audio_config
		)

		filename = f"{name}.wav"
		with open(filename, "wb") as out:
			out.write(response.audio_content)
			print(f'Audio content written to "{name}"')

if __name__=="__main__":
	synthesizer = GoogleVoice()
	synthesizer.list_languages()
	synthesizer.list_voices("en")	
