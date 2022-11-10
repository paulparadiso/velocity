from configurablecomponent import ConfigurableComponent

class InputController(ConfigurableComponent):

	def __init__(self, clips=None):
		super().__init__()
		self.clips = []
		self.next_clip = 0

	def get_clips(self):
		return self.clips

	def get_next_clip(self):
		return next_clip

	def add_clip(self, clip):
		pass

	def update_clip(self, clip):
		pass

	def remove_clip(self, clip):
		pass