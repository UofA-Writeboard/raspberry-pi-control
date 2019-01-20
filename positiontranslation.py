import math

from point import Point


class PositionTranslation(object):
	def __init__(self, spool_width=1280, spool_dia=20, counts_per_rev=2400):
		self.width = spool_width
		self.radius = spool_dia/2
		self.circumfrance = 2 * math.pi * self.radius
		self.counts = counts_per_rev
		self.count_per_mm = self.counts / self.circumfrance

		# left, right looking at the board
		self.home_pos = Point(0, 800)
		self.offset_length = 0, 0
		self.home(self.home_pos)

	def home(self, pos=Point(0, 800)):
		self.home_pos = pos

		offset_l1, offset_l2 = self.pos_to_len(self.home_pos)

		self.offset_length = offset_l1, offset_l2

	def pos_to_len(self, pos):
		l1 = math.sqrt(pos.y ** 2 + (pos.x + (self.width / 2))**2)
		l2 = math.sqrt(pos.y ** 2 + (pos.x - (self.width / 2))**2)
		# left, right looking at the board
		return l1, l2

	def pos_to_rad(self, pos):
		l1, l2 = self.pos_to_len(pos)
		l1 = l1 - self.offset_length[0]
		l2 = l2 - self.offset_length[1]
		rot_1_steps = l1 * self.count_per_mm
		rot_2_steps = l2 * self.count_per_mm

		return rot_1_steps, rot_2_steps

if __name__ == '__main__':
	pos_trans = PositionTranslation()
	board_height = 855.7
	pos_trans.home(Point(0, board_height))

	print pos_trans.pos_to_rad(Point(-500, 700))
