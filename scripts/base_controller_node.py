#!/usr/bin/env python

import rospy
import MD25
import datetime
from geometry_msgs.msg import Twist

class RobotBase:

	def __init__(self, controller, wheel_separation, wheel_diameter=.1):
		self.controller = controller
		self.wheel_base = wheel_dist / 2
		self.wheel_radius = wheel_diameter /2
		self.micros = float(datetime.datetime.now().microsecond) / 1000000
		self.last_micros = self.delta_time
		self.max_speed = 170 * (1/60) * 2 * math.Pi * self.wheel_radius

	def _delta_time(self):
		self.last_micros = self.micros
		self.micros = float(datetime.datetime.now().microsecond) / 1000000
		assert self.last_micros is not self.micros
		return self.micros - self.last_micros

	def wheel_speed(self):
		return (count * self.resolution * self._delta_time() * self.wheel_radius for count in self.delta_count())

	def set_speed(self, speed):
		"""Takes speed in m/s and sets appropriate level"""
		if speed > self.maxspeed:
			# Print a warning in ROS that the base is being requested to drive faster than it can
			pass
		self.throttle((speed / self.max_speed * 128) + 128)

	def set_turn_rate(self, omega):
		"""Takes rad/s turn rate and sets appropriate level"""
		self.turn_amount(((omega * self.wheel_base) / self.max_speed * 128) + 128)


def callback(msg):
	rospy.loginfo("throttle: %s, int %s", msg.linear.x, int(msg.linear.x))
	md25.throttle(int(msg.linear.x))
	md25.turn_amount(int(msg.angular.z))

def controller_node():
	rospy.init_node("base_controller")

	# Subscribe to /joy, /cmd_vel
	rospy.Subscriber("cmd_vel", Twist, callback)

	#TODO: extract the axes info from the Joy msg and use it to set speed
	# Linear: x, y, z -> linear x [m/s]
	# Angular x, y, z -> angular z [rad/s]

	# publish to /odom, tf, batterystate

	rospy.spin()
	pass

if __name__ == '__main__':
	md25 = MD25.MD25()
	try:
		controller_node()
	except rospy.ROSInterruptException:
		rospy.loginfo("Shutting down...")

