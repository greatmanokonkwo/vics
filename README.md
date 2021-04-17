# V.I.C.S (Visual Impairment Companion System)
![VICS LOGO](vics_logo.gif)
 
**Powered by Nvidia**

VICS is an end-to-end learning based visual impairment device that strives to make the world more accessible to the visually impaired. VICS is currently made up of three separate systems that work to bring the world to the user via a suite of information rallying devices including vibration motors and speech enabled assistance.

## Running on native machine

### Pytorch for Jetson nano

*Instructions from https://forums.developer.nvidia.com/t/pytorch-for-jetson-version-1-7-0-now-available/72048*

Install PyTorch pip wheel v1.7.0

```
wget https://nvidia.box.com/shared/static/cs3xn3td6sfgtene6jdvsxlr366m2dhq.whl -O torch-1.7.0-cp36-cp36m-linux_aarch64.whl
sudo apt-get install python3-pip libopenblas-base libopenmpi-dev 
pip3 install Cython
pip3 install numpy torch-1.7.0-cp36-cp36m-linux_aarch64.whl
```
Install torchvision
```
sudo apt-get install libjpeg-dev zlib1g-dev libpython3-dev libavcodec-dev libavformat-dev libswscale-dev
git clone --branch v0.8.1 https://github.com/pytorch/vision torchvision   # see below for version of torchvision to download
cd torchvision
export BUILD_VERSION=0.8.1
sudo python3 setup.py install    
cd ../ 
```

### pip install packages
```
sudo apt-get install portaudio19-dev
pip3 install --user --upgrade -r requirements.txt
```

### Google Cloud Text-to-Speech API key

```
wget https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-329.0.0-linux-x86_64.tar.gz
tar -xvzf google-cloud-sdk-329.0.0-linux-x86_64.tar.gz
./google-cloud-sdk/install.sh
(Select mystical-ace-305717 project)
./google-cloud-sdk/bin/gcloud init
source ~/.bashrc
gcloud auth list
gcloud config list project
gcloud services enable texttospeech.googleapis.com
echo "export PROJECT_ID=$(gcloud config get-value core/project)" > ~/.bashrc
gcloud iam service-accounts keys create ~/key.json --iam-account my-tts-sa@${PROJECT_ID}.iam.gserviceaccount.com
export GOOGLE_APPLICATION_CREDENTIALS=~/key.json
echo export GOOGLE_APPLICATION_CREDENTIALS=~/key.json > ~/.bashrc
```

### Google Tesseract-OCR Engine
```
sudo apt get install tesseract-ocr
sudo apt-get install libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev
wget https://github.com/ZER-0-NE/EAST-Detector-for-text-detection-using-OpenCV/blob/master/frozen_east_text_detection.pb
```

### YOLOV3 weights file

Download the weights file in ``vics/speech_and_comms/scene_describe_system/weights``

```
wget https://pjreddie.com/media/files/yolov3-tiny.weights
```
## TO-DO 
**NOTE:** All tasks involving the GPS Guidance System should be held off until everything else has been completed. This is only an extension of the project.

### General Hardware

- [x] Jetson Nano Developer Kit 4-GB
- [ ] Design rechargeable battery / buy a rechargeable battery

### 1. Direction Planning System

#### Software 

- [x] Implement AlexNet architecture for Direction Planning (direction_plan/neuralnet/model.py) 
- [x] Write training process for the Direction Planning System (direction_plan/neuralnet/train.py)
- [x] Interface vibration motor for halt signalling (direction_plan/devices/vibrator_motor.py)
- [x] Finish up mpu6050 code to enable calculation of Yaw angle (direction_plan/devices/mpu6050.py)
- [x] Figure out halt signal calculations (direction_plan/collect_data.py)
- [x] Build direction_plan interfacing engine (direction_plan/engine.py)
- [ ] Collect data (data such as stopping at cross walks and roads be very helpful)

#### Hardware

- [x] MPU9250 9-axis IMU sensor
- [x] Raspberry Pi Camera
- [x] 2x Vibration motors
- [x] Get and setup Macro/Wide lens for Pi Camera

### 2. Speech and Communications Systems (Voice Assistant and Scene Description)

#### Sofware

- [x] Interface with microphone hardware
- [x] Interface with speaker hardware
- [x] Write object detection model 
- [ ] Build WakeWord model for AI voice assistant (wake word: "Hey VICS")
- [ ] Build NLP model for taking in audio input and return a classification for the command issued
- [x] Using the detected objects find way to create voice responses with the detected objects
- [x] Write data collection scripts

#### Hardware

- [x] SPH0645LM4H MEMS Microphone
- [x] MAX98357A Amflifier

### Product Design

#### Software

- [x] Design CAD for Enclosure using FreeCAD

#### Hardware

- [x] Create chest mount straps
- [x] 3d print Enclosure
