from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np

from linearinterpolator import LinearInterpolator
from point import Point

class MomentChain(object):
	def __init__(self, start_pos):
		self.start_pos = start_pos
		self.cords = list()

	def append(self, item):
		self.cords.append(item)


class GcodeInterpreter(object):
	def __init__(self, filename):
		# number of mm per unit distance
		self.unit_mul = 1
		self.g_code_cords = list()
		with open(filename, "r") as f:
			current_chain = None
			for line in f:
				line = line.strip()
				if line.startswith("G21"):
					self.unit_mul = 1
				elif line.startswith("G20"):
					self.unit_mul = 25.4
				elif line.startswith("G00"):
					res = self.parse_g(line, self.unit_mul)
					if res is not None:
						if current_chain is not None:
							self.g_code_cords.append(current_chain)
						current_chain = MomentChain(res)
				elif line.startswith("G01"):
					res = self.parse_g(line, self.unit_mul)
					if res is not None:
						if current_chain is None:
							current_chain = MomentChain(res)
						else:
							current_chain.append(res)
				else:
					pass
					print "------ unknown command {} ------".format(line)
			if current_chain is not None:
				self.g_code_cords.append(current_chain)
		self.cords = [self.interpolate_lines(chain) for chain in self.g_code_cords]
		# self.cords = [self.interpolate_lines(self.g_code_cords[0])]


	@staticmethod
	def interpolate_lines(chain):
		output = MomentChain(chain.start_pos)
		last_point = chain.start_pos
		for segment in chain.cords:
			output.cords.extend(LinearInterpolator(last_point, segment).interpolated_points())
			last_point = segment
		return output

	@staticmethod
	def parse_g(line, scale):
		# print "------ parsing {} ------".format(line)
		x = None
		y = None
		for segment in line.split():
			segment = segment.lower()
			if segment.startswith("x"):
				x = float(segment[1:])
			elif segment.startswith("y"):
				y = float(segment[1:])
			else:
				if segment[0] not in ["z", "f", "g"]:
					print "unrecognized segment {} in {}".format(segment, line)
		if x is not None and y is not None:
			return Point(x*scale, y*scale)
		else:
			return None


def plot_int(int):
	for item in int:
		x_list = list()
		y_list = list()

		x_list.append(item.start_pos.x)
		y_list.append(item.start_pos.y)

		for p in item.cords:
			x_list.append(p.x)
			y_list.append(p.y)

		plt.plot(x_list, y_list, color='red', marker='.')


if __name__ == '__main__':
	int = GcodeInterpreter("test.gcode")
	plot_int(int.cords)
	plt.show()

