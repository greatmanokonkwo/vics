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
git clone --branch <version> https://github.com/pytorch/vision torchvision   # see below for version of torchvision to download
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

- [ ] Interface with microphone hardware
- [x] Interface with speaker hardware
- [x] Write object detection model 
- [ ] Build WakeWord model for AI voice assistant (wake word: "Hey VICS")
- [ ] Build NLP model for taking in audio input and return a classification for the command issued
- [x] Using the detected objects find way to create voice responses with the detected objects
- [ ] Write data collection scripts

#### Hardware

- [x] SPH0645LM4H MEMS Microphone
- [x] MAX98357A Amflifier

### Product Design

#### Software

- [ ] Design CAD for Enclosure using Fusion 360

#### Hardware

- [ ] Create chest mount straps
- [ ] 3d print Enclosure

## Vision and Purpose

According to the World Health Organization (WHO) there are an estimated 285 million people who are visually impaired globally, 39 million of whom are completely blind. As you can expect, the visually impaired find it very hard to get around. Many tools have been developed to aid the visually impaired navigate, perceive and understand their environments. An example of methods used for helping the visually impaired navigate is the good old walking stick and guide dog. The problem with walking sticks is that they give little navigation data and they only inform the user about whats below them, however they are very affordable, most coming in at about $30. Guide dogs are a lot more useful as they help the user get around quickly by navigating the terrain for the user. However, guide dogs are very expensive to get and maintain. This is due to the number of hours of specialized training needed. In Canada, it takes about two years and costs up to $35,000 to train a guide dog. This results in low supply of a service that is very much in high demand. The visually impaired struggle with reading text. Methods such as braille and braille printers have been very useful in this area but their ultility starts to dwindle as we move to the realm of computer and phone screens. Also, most things such as text in the real world is not readilty converted to braille. 

We have worked hard to tackle these challenges using novel methods that enable the visually impaired to interact with their environment in a safe, reliable and affordable manner. That is why we are introducing VICS, the Visual Impairment Companion System. VICS is a system that is made up of a collection of tools that provide navigation, perception and reading services in a user friendly manner. In particular, VICS is equipped with a guide system that tells the user the direction they should move in to avoid obstacles. It also contains an object detection and speech system that takes an image of a scene and rallys to the user the names, location and proximity of all detected objects in the scene through voice synthesis. Finally, the VICS can take an image of whatever the user wants to read and read the detected text out loud for the user to listen. It truly is an all around companion to the visually impaired. But that is not what makes the VICS special. Most of the tasks mentioned above have been done before. Autonomous robots exists that can navigate their environments. There are devices that can detect objects and their distances from them. Finally, OCR has been around since Ray Kutzerweil invented it in 1975. The VICS is special because it accomplished all these tasks using a single camera and an IMU sensor, which in total cost approximately $50 in total. Automous navigation methods rely on heavy and expensive sensor suites that include LiDAR and Depth Cameras. Cheap 2D-Lidar comes at about $100> a pop, and the story is the same for depth cameras. A large suite also carries weight, making it hard to turn into a portable device. Imagine walking around with a huge LiDAR sensor on your chest that is loudly and obnoxiously doing about 10 rotations a second. This has made navigation systems a feature for robots and larger vehicles. However, we present a new method for autonomouse navigation that relies only on the RGB outputs of a standard camera. We use an end-to-end deep learning method take as input an image of a scene and outputs the direction that needs to been taken in order to safely navigate the scene. We accomplish this by collecting lots of image and direction data points and training a convolutional neuralnet on them. (Insert measured accuracy of device). 

Using deep learning technology we were able to ensure that the VICS was a cheap and practical solution for a visual aid service. See below the VICS device. It is composed of the actually device that houses all the necessary components as well as a chest mount for when the user wants to use its navigation features. The VICS can be used as a stand alone device for peforming its scene description and text reading tasks. When the user needs to navigate using the VICS, they can connect it to the chest mount which houses vibration motors for rallying the direction that needs to be taken by the user.

