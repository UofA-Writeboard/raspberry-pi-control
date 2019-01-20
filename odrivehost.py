import odrive


class OdriveHost(object):
	def __init__(self, odrv):
		self.odrv = odrv
		self.reset_home()
		self.m0_offset = 0
		self.m1_offset = 0

	def reset_home(self):
		self.m0_offset = self.odrv.axis0.controller.pos_setpoint
		self.m1_offset = self.odrv.axis1.controller.pos_setpoint

	def goto(self, m0, m1, tol=3):
		self.odrv.axis0.controller.move_to_pos(self.m0_offset - (-1 * m0))
		self.odrv.axis1.controller.move_to_pos(self.m1_offset - (1 * m1))
		while abs(self.odrv.axis0.encoder.pos_estimate - (self.m0_offset - (-1 * m0))) > tol or \
				abs(self.odrv.axis1.encoder.pos_estimate - (self.m1_offset - (1 * m1))) > tol:
			pass

	def pos_set(self, m0, m1):
		self.odrv.axis0.controller.pos_setpoint = (self.m0_offset - (-1 * m0))
		self.odrv.axis1.controller.pos_setpoint = (self.m1_offset - (1 * m1))
