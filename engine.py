import os
import time
import threading
import playsound
<<<<<<< HEAD
#import Jetson.GPIO as GPIO
=======
import Jetson.GPIO as GPIO
>>>>>>> 40c4c125e3f3837dbdf28e6be73a6f1a5c234e21
import pyaudio
import wave

import torch
import torchaudio

<<<<<<< HEAD
import wakeword.engine
from wakeword import neuralnet
import command_processor
import guide 
import describe  
import read 

from devs_and_utils.picam import picam
from devs_and_utils.audio_utils import get_featurizer
from devs_and_utils.google_voice import GoogleVoice
=======
from wakeword.engine import WakeWordEngine, DemoAction
from command_processor.engine import LSTMCommands
from guide.engine import GuideSystem
from describe.engine import SceneDescribeSystem 
from read.engine import ReadingSystem

from devs_and_utils.picam import picam
from devs_and_utils.audio_utils import get_featurizer
>>>>>>> 40c4c125e3f3837dbdf28e6be73a6f1a5c234e21

"""
COMMAND 0 (Guide): This enable to GuideNet process that relays angles of direction to travel in to the user, using vibrations
COMMAND 1 (Describe): This enables the Scene description process, that detects various objects in front of the user and using voice, tells what these objects are and where they are located (left, center, right) relative to them
COMMAND 2 (Read): This enables to reading process which takes a picture of whatever is in front of the VICS gear camera and reads the text in the image
"""
# Global Variables

WAKEWORD_DETECTED = False
device = "cuda" if torch.cuda.is_available() else "cpu"

# General tools and devices 
cam = picam(width=1028, height=1028)

voice = GoogleVoice()
voice_name = "en-GB-Standard-B"

audio_transform = get_featurizer(8000)

# System Modules
## Wakeword
wakeword_engine = WakeWordEngine()

## Commands Detector
command_names = ["Guide Me", "Describe the Scene", "Read this"]

model_params = {
	"num_classes": 3, "feature_size": 40, "hidden_size": 128,
	"num_layers": 1, "dropout": 0.1, "bidirectional": False
}
<<<<<<< HEAD
commands_model = command_processor.engine.LSTMCommands(**model_params, device=device)
=======
commands_model = LSTMCommands(**model_params, device=device)
>>>>>>> 40c4c125e3f3837dbdf28e6be73a6f1a5c234e21
params_path = "commands_processor/neuralnet/commands.pt"

commands_model.load_state_dict(torch.load(params_path)["model_state_dict"])
commands_model = model.to(device)

audio_transform = get_featurizer(8000)

## Guidance System
<<<<<<< HEAD
guide = GuideSystem()
=======
guide = GuideSystem
>>>>>>> 40c4c125e3f3837dbdf28e6be73a6f1a5c234e21

## Scene Description System
describe = SceneDescribeSystem()

## Reading system
read = ReadingSytem()

# Module Functions

## WakeWord 
def wakeword_action(prediction):
	if prediction == 1:
		WAKEWORD_DETECTED = True
		playsound("devs_and_utils/presets/greet.wav")
		command = threading.Thread(target=commands_run, args=())
		print("Starting Command Sequence ...")
		WAKEWORD_DETECTED = False
		command.start()
	
## Commands Detector
def record_audio(seconds=5):
	chunk = 1024
	sample_format = pyaudio.paInt16
	channels = 1
	fs = 8000
	filename = "voice_command.wav"
	
	p = pyaudio.PyAudio()
	
	print("Recording")
	
	stream = p.open(format=sample_format,
					channels=channels,
					rate=fs,
					frames_per_buffer=chunk,
					input=True)
		
	frames = []
	
	for i in range(0, int(fs/chunk * seconds)):
		data = stream.read(chunk)
		frames.append(data)
	
	stream.stop_stream()
	stream.close()
		
	p.terminate()
	
	print("Finished recording")
	
	wf = wave.open(filename, "wb")
	wf.setnchannels(channels)
	wf.setsampwidth(p.get_sample_size(sample_format))
	wf.setframerate(fs)
	wf.writeframes(b''.join(frames))
	wf.close()

def open_and_transform_audio():
	# Transform the recorded audio for inference by commands detection model
	waveform, sr = torchaudio.load("voice_command.wav")
	os.remove("voice_command.wav")
	mfcc = audio_transform(waveform).transpose(1, 2).transpose(0, 1)
	mfcc = mfcc.to(device)	

	return mfcc

def commands_run():
	global WAKEWORD_DETECTED # Main thread will change this signal if the wakeword is detected, prompting function to stop executing

	# Record Audio for voice command
	record_audio()
	start_t = time.time()
	output = commands_model(open_and_transform_audio())[0]

	_, pred = torch.max(torch.sigmoid(output), dim=1)
	print(f"[INFO] Detected \"{commands_names[pred]}\" command in {start_t - time.time()} seconds!")

	if pred == 0:
		# Play preset response
		playsound("devs_and_utils/presets/guide.wav")

		while WAKEWORD_DETECTED == False:
			guide.run(cam)
			
	else:
		if pred == 1:
			playsound("devs_and_utils/presets/describe.wav")
<<<<<<< HEAD
		elif pred == 2:
=======
		else pred == 2:
>>>>>>> 40c4c125e3f3837dbdf28e6be73a6f1a5c234e21
			playsound("devs_and_utils/presets/read.wav")

		start_t = time.time()

		if pred == 1:
			response = describe.run(cam=cam)
			print("[INFO] Scene Description detected objects in {start_t - time.time()} seconds!")
<<<<<<< HEAD
		elif pred == 2:
=======
		else if pred == 2:
>>>>>>> 40c4c125e3f3837dbdf28e6be73a6f1a5c234e21
			response = read.run(cam=cam)
			print("[INFO] eading completed in {start_t - time.time()} seconds!")

		voice.text_to_speech(voice_name=voice_name, text=response, name="response") # Turn generated response to speech
		playsound("response.wav") # play response on speakers
		os.remove("response.wav") # Delete generate response file


if __name__ == "__main__":
	print("Settting up device ... this should take a few seconds")
	read.run()

	action = wakeword_action() # This action is called by the wakeword whenever it makes a prediction. It activates the command detection and run sequence
	wakeword_engine.run(action)	
	threading.Event().wait()
