import numpy as np

# mm/s/s
acc_g = 9000

# mm/s
v_max = 3000

class MotionPlanning(object):
	def __init__(self, chain):
		self.chain = chain
		self.acc_array = np.zeros((len(chain.cords), 2))
		self.vel_array = np.zeros((len(chain.cords), 2))

		self.pos_array = [pt for pt in self.chain.cords]

		last_point = chain.start_pos

		for i, pos in enumerate(self.pos_array):

			self.vel_array[i+1] = self.vel_array[i]**2 + 2 * self.vel_array[i] * last_point.dist(pos)
