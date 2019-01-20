import time
import math

import RPi.GPIO as GPIO
import odrive
import boto3

from odrivehost import OdriveHost
from positiontranslation import PositionTranslation
from gcodeinterpreter import GcodeInterpreter
from point import Point

board_height = 855.7

pwm_off = 10
pwm_on = 6

# Setup PWM
servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)
# 50Hz PWM
servo_pwm = GPIO.PWM(servoPIN, 50)
servo_pwm.start(2.5)
servo_pwm.ChangeDutyCycle(pwm_off)


def PointsInCircum(r, x_in=0, y=0, n=100):
	points = [(math.cos(2*math.pi/n*x)*r, math.sin(2*math.pi/n*x)*r) for x in range(0, n+1)]
	points = [(p_x + x_in, p_y + y) for p_x, p_y in points]
	return points


def run_momentchain(chain):
	pos_trans = PositionTranslation()
	pos_trans.home(Point(0, board_height))
	host.goto(*pos_trans.pos_to_rad(chain.start_pos))
	# time.sleep(5)
	servo_pwm.ChangeDutyCycle(pwm_on)
	time.sleep(0.25)
	for p in chain.cords:
		host.pos_set(*pos_trans.pos_to_rad(p))
		time.sleep(0.0025)

	servo_pwm.ChangeDutyCycle(pwm_off)
	time.sleep(0.25)


if __name__ == '__main__':
	print "Finding odrives!"
	odrv0 = odrive.find_any()
	print "Found!"

	host = OdriveHost(odrv0)
	host.reset_home()

	test = False

	if test:
		pass
	else:
		sqs = boto3.resource('sqs')
		queue = sqs.get_queue_by_name(QueueName='WriteboardTest')

	try:
		if test:
			int = GcodeInterpreter("test.gcode").cords
			for chain in int:
				run_momentchain(chain)
		else:
			while 1:
				host.goto(0, 200)
				for message in queue.receive_messages(MessageAttributeNames=['Author']):
					print "Got a message!"
					with open("test.gcode", "w") as f:
						f.write(message.body)
					int = GcodeInterpreter("test.gcode").cords
					for chain in int:
						run_momentchain(chain)
					message.delete()
	finally:
		servo_pwm.ChangeDutyCycle(pwm_off)
		time.sleep(0.25)
		host.goto(0, 0)
