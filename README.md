# V.I.C.S (Visual Impairment Companion System)
![VICS LOGO](vics_logo.gif)
 
**Powered by Nvidia**

VICS is an end-to-end learning based visual impairment device that strives that make the world more accessible to people who are visually impaired. VICS is currently made up of three separate systems that work to bring the world to the user via a suite of information rallying devices including vibration motors and speech enabled assistance.

## TO-DO 

### 1. Direction Planning System

#### Software 

- Implement AlexNet architecture for Direction Planning (direction_plan/neuralnet/model.py) 
- Write training process for the Direction Planning System (direction_plan/neuralnet/train.py)
- Interface vibration motor for halt signalling (direction_plan/devices/vibrator_motor.py)
- Finish up mpu6050 code to enable calculation of Yaw angle (direction_plan/devices/mpu6050.py)
- Figure out halt signal calculations (direction_plan/collect_data.py)
- Build direction_plan interfacing engine (direction_plan/engine.py)

#### Hardware

- Get and setup Macro/Wide lens for Pi Camera
- Consider switching to a 9-axis sensor with acceloremeter, gyroscope and magnometer
- Figure out powering servo motor
- Figure out interfacing servo motor (Wired/Wireless?)

### 2. Speech and Communications System

#### Sofware

- Interface with mircrophone hardware
- Interface with speaker hardware
- Build wakeword system to activate system when user says "Hey VICS!"
- Write scene description voice command
- Write GPS guidance voice command

#### Hardware

- Buy mircrophone hardware
- Buy speaker hardware

### 3. GPS Guidance System

#### Software

- Interface with GPS receiver
- Gain access to google maps
- Wireless network connection?
- GPS Tracking
- GPS Guidance engine with Direction Planning System

#### Hardware

- Get GPS receiver
- Wi-Fi connection module

### Design

- Build chest mount
- Plastic back cover for hardware to be mounted on
- Handle for servo motor gear 
