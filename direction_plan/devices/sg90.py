# Import Revelant Libraries
import Jetson.GPIO
import time 

# Servo Motor (sg90) class
class sg90:
	# Private variables
	_servo = None

	_PWM_PIN = None
	_PULSE_FREQ = 50
	_MIN_DUTY = 2 # The lower bound for the range of duty cycle

	_degree_to_duty = lambda theta : theta/18 + MIN_DUTY

	def __init__(self, start_deg=0, gpio_pin_=32):
		# Set GPIO pin that is configured for PWM. Default for Jetson Nano is Pin 32
		self._PWM_PIN = gpio_pin_

		# Set GPIO numbering mode
		Jetson.GPIO.setmode(Jetson.GPIO.BOARD) 

		# Set gpio_pin as an output, and set servo as pin 32 as PWM
		Jetson.GPIO.setup(self._PWM_PIN,Jetson.GPIO.OUT)
		self.servo = Jetson.GPIO.PWM(self._PWM_PIN,self._PULSE_FREQ)

		# Start PWM running, but with value of start_freq (default 0 or pulse off)
		self.servo.start(self._degree_to_duty(start_deg))

	def _degree_to_duty(self, degree):
		return degree/18 + self._MIN_DUTY 

	def rotate(self, degree, sleep_time=0):
		# Rotate servo motor
		self.servo.ChangeDutyCycle(self._degree_to_duty(degree))
	
		# Optional program sleep
		time.sleep(sleep_time)

	def clean(self):
		# Cleanup things once done using
		self.servo.stop()
		Jetson.GPIO.cleanup() 
