import os
os.sys.path.append("..")

import torch
import pyaudio
import wave
import torchaudio
from neuralnet.model import LSTMCommands

from devs_and_utils.audio_utils import get_featurizer

device = "cuda" if torch.cuda.is_available() else "cpu"
audio_transform = get_featurizer(8000)
	
def record_audio():
	chunk = 1024
	sample_format = pyaudio.paInt16
	channels = 1
	fs = 8000
	seconds = 5
	filename = "output.wav"
	
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
	waveform, sr = torchaudio.load("output.wav")
	mfcc = audio_transform(waveform).transpose(1, 2).transpose(0, 1)
	mfcc = mfcc.to(device)	

	print(mfcc.shape)

	return mfcc

if __name__ == "__main__":
	model_params = {
		"num_classes": 3, "feature_size": 40, "hidden_size": 128,
		"num_layers": 1, "dropout": 0.1, "bidirectional": False
	}

	model = LSTMCommands(**model_params, device=device)
	params_path = "neuralnet/commands.pt"

	model.load_state_dict(torch.load(params_path)["model_state_dict"])
	model = model.to(device)

	record_audio()
	output = model(open_and_transform_audio())[0]

	class_names = ["Guide Me", "Describe the Scene", "Read this"]	
	_, pred = torch.max(torch.sigmoid(output), dim=1)
	print(class_names[pred])
