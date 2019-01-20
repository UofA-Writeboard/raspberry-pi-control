import math
import sys


class Point(object):
	# Units are all in mm
	def __init__(self, x, y, t=None):
		self.x = x
		self.y = y
		self.t = t

	def dist(self, point):
		return math.sqrt((self.x - point.x)**2 + (self.y - point.y)**2)

	def slope(self, point):
		try:
			return (point.y - self.y) / (point.x - self.x)
		except ZeroDivisionError:
			return sys.float_info.max

	def __str__(self):
		return "({}, {})".format(self.x, self.y)

	def __repr__(self):
		return "Point({}, {})".format(self.x, self.y)

	@property
	def xy(self):
		return self.x, self.y

if __name__ == '__main__':
	a = Point(1, 1)
	b = Point(1, 5)
	print a.slope(b)