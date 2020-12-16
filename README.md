# V.I.C.S (Visual Impairment Companion System)
![VICS LOGO](vics_logo.gif)
 
**Powered by Nvidia**

VICS is an end-to-end learning based visual impairment device that strives that make the world more accessible to people who are visually impaired. VICS is currently made up of three separate systems that work to bring the world to the user via a suite of information rallying devices including vibration motors and speech enabled assistance.

## TO-DO 
**NOTE:** All tasks involving the GPS Guidance System should be held off until everything else has been completed. This is only an extension of the project.

### General Hardware

- [x] Jetson Nano Developer Kit 4-GB
- [ ] Design rechargeable battery / buy a rechargeable battery

### 1. Direction Planning System

#### Software 

- [ ] Implement AlexNet architecture for Direction Planning (direction_plan/neuralnet/model.py) 
- [ ] Write training process for the Direction Planning System (direction_plan/neuralnet/train.py)
- [ ] Interface vibration motor for halt signalling (direction_plan/devices/vibrator_motor.py)
- [ ] Finish up mpu6050 code to enable calculation of Yaw angle (direction_plan/devices/mpu6050.py)
- [ ] Figure out halt signal calculations (direction_plan/collect_data.py)
- [ ] Build direction_plan interfacing engine (direction_plan/engine.py)
- [ ] Collect data (data such as stopping at cross walks and roads be very helpful)

#### Hardware

- [x] MPU-6050 6-axis accelorometer and gyroscope
- [x] Raspberry Pi Camera
- [x] 2x Vibration motors
- [ ] Get and setup Macro/Wide lens for Pi Camera
- [ ] Consider switching to a 9-axis sensor with acceloremeter, gyroscope and magnometer (MPU9250)

### 2. Speech and Communications System (Voice Assistant and Scene Description)

#### Sofware

- [ ] Interface with microphone hardware
- [ ] Interface with speaker hardware
- [ ] Build object detection model as well as object location algorithm
- [ ] Build WakeWord model for AI voice assistant (wake word: "Hey VICS")
- [ ] Build Speech Recognition model to turn audio to text
- [ ] Build NLP model to understand the voice commands "Describe" (Will add command for get directions to a place on google maps "Take to the closest Donut Shop")
- [ ] Build Speech Synthesis model that can say things like "There is a table in the top-left view and a door in the center view" or "The Donut Shop is 6min away, go outside and we can start walking" or "You have reached your destination"
- [ ] Write data collection scripts

#### Hardware

- [ ] Electret Microphone Amplifier - MAX4466
- [ ] Bone Conductor Transducer

### 3. GPS Guidance System

#### Software

- [ ] Interface with GPS receiver
- [ ] Gain access to google directions API
- [ ] Interface with Directions API
- [ ] Write Destination vector and obstacle vector fusion algorithm (We need to get the user to the destination while also avoiding obstacles. Desired Vector - Target Vector)
- [ ] Wireless connection module 
- [ ] Directions should be downloaded prior to starting the journey, because Internet connection will be lost!
- [ ] GPS Tracking with GPS receiver
- [ ] GPS Guidance engine with Direction Planning System

#### Hardware

- [ ] GPS Receiver
- [ ] Wi-Fi Module

### Product Design

#### Software

- [ ] Design CAD for Enclosure using Fusion 360

#### Hardware

- [ ] Create chest mount straps
- [ ] 3d print Enclosure
