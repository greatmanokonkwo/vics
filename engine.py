import requests
import Jetson.GPIO as GPIO

from speech_and_comms.wakeword.engine import WakeWordProcessor
from speech_and_comms.command_processor.engine import CommandProcessor
from guide_system.engine import GuideSystem
from speech_and_comms.scene_describe_system.engine import SceneDescribeSystem 
from speech_and_comms.image_reading_system.engine import ImageReadingSystem


"""
COMMAND 0 (Guide): This enable to GuideNet process that relays angles of direction to travel in to the user, using vibrations
COMMAND 1 (Describe): This enables the Scene description process, that detects various objects in front of the user and using voice, tells what these objects are and where they are located (left, center, right) relative to them
COMMAND 2 (Read): This enables to reading process which takes a picture of whatever is in front of the VICS gear camera and reads the text in the image

ONLINE MODE: This mode supports all three commands and enhances command 1 with the google text to speech API
OFFLINE MODE: This mode only supports the first 2 commands and uses downloaded premade reponses for each object-position possibility

""" 

# For ONLINE MODE 
WAKEWORD_DETECTED = False

# For OFFLINE MODE. Guidance System is turned on automatically in offline mode
## GPIO pin for guidance system button
BUTTON0 = 38

## GPIO pin for scene description button
BUTTON1 = 40

# Command execution engines
GUIDE = GuideSystem()
DESCRIBE = SceneDescribeSystem() 
READ = ImageReadingSystem()

# Audio stream processors
WAKE = WakeWord()
COMMAND = CommandProcessor()

def check_connection():
	url = "https://github.com/greatmanokonkwo/vics"
	timeout = 5
	try:
		request = requests.get(url, timeout=timeout)
		print("Connected to the Internet")
		return True
	except (requests.ConnectionError, requests.Timeout) as exception:
		print("No internet connection.")
		return False

def wakeword_detect:
	# TODO: Add wakeword detection process

	# This process is responsible for changing the WAKEWORD_DETECTED signal 

if __name__=="__main__":
	# Online Mode 
	# The Online Mode is supported by a voice assistant that can respond the voice requests of the user in order to execute commands
	if (check_connection()):

		# Start wakeword detection process on another thread. This process is responsible for alerting the command execution process to either start or stop a command
		
		# Continously loop, waiting for wakeword to give wakeword detected signal
		while True:
			if WAKEWORD_DETECTED:
				WAKEWORD_DETECTED = False

				# TODO: Add command detection process and set result to variable command
				command = COMMAND.run()
				
				if command == 0:
					# Guidance system runs indefinitely until the wakeword is detected
					while WAKEWORD_DETECTED == False:
						GUIDE.run()

				else if command == 1:
					# TODO: Add scene description process	
					DESCRIBE.run()

				else if command == 2:
					# TODO: Add reading process 
					READ.run()

	# Offline Mode
	# The Offline Mode is supported by two side buttons on the VICS gear enclosure that signal the execution of processes
	else:
		# Set up GPIO pins for the buttons
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(BUTTON0, GPIO.IN, initial=GPIO.LOW)
		GPIO.setup(BUTTON1, GPIO.IN, initial=GPIO.LOW)  

		# Stores state of buttons
		button0 = GPIO.input(BUTTON0)
		button1 = GPIO.input(BUTTON1)

		# Activate command 0 or 1
		activate0 = 0
		activate1 = 0

		while True:
			current0 = GPIO.input(BUTTON0)
			current1 = GPIO.input(BUTTON1)

			# If a button changes its state, set its process' activation to that state and set the activation of the other process' to 0
			if button0 != current0:
				activate0 = current0
				activate1 = GPIO.LOW
		
			if button1 != current1:
				activate0 = GPIO.LOW
				activate1 = current1
		
			button0 = current0
			button1 = current1
	
			if activate0:
				# Run guidance process
				GUIDE.run()
	
			else if activate1:
				# Run objection detectoin process
				DESCRIBE.run()
							
