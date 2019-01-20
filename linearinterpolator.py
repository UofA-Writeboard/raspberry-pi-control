import matplotlib.pyplot as plt
import numpy as np

from point import Point
import math

class LinearInterpolator(object):
	def __init__(self, start, end, interpolation=0.25):
		self.reverse = False
		if end.x < start.x:
			start, end = end, start
			self.reverse = True
		self.start = start
		self.end = end
		self.inter_dist = interpolation

	def interpolated_points(self):
		number_of_points = math.ceil(self.start.dist(self.end)/self.inter_dist)
		if number_of_points < 2:
			number_of_points = 2
		# print "Start: {}".format(self.start)
		# print "End: {}".format(self.end)
		if self.start.slope(self.end) < 1:
			xinterp = np.linspace(self.start.x, self.end.x, num=number_of_points)
			yinterp = np.interp(xinterp, [self.start.x, self.end.x], [self.start.y, self.end.y])
		else:
			yinterp = np.linspace(self.start.y, self.end.y, num=number_of_points)
			xinterp = np.interp(yinterp, [self.start.y, self.end.y], [self.start.x, self.end.x])
		# plt.scatter(xinterp, yinterp)
		# plt.plot([self.start.x, self.end.x], [self.start.y, self.end.y], color='red', marker='.')
		# plt.show()
		int_points = list()
		for x, y in zip(xinterp, yinterp):
			int_points.append(Point(x, y))
		if self.reverse:
			int_points = int_points[::-1]
		return int_points


if __name__ == '__main__':
	import struct

	print struct.calcsize("P") * 8
	start = Point(44.100667, 226.554416)
	end = Point(43.966307, 220.978531)

	x = LinearInterpolator(start, end)
	x.interpolated_points()
