from playlistcontroller import PlaylistController
from oscreceiver import OSCReceiver
from arenacontroller import ArenaController

modes = [
	'Playlist',
	'OBD'
]

class ClipManager:

	def __init__(self, mode='Playlist', master_ip='127.0.0.1', arena_controller=None):
		self.controllers = {}
		self.controllers['Playlist'] = PlaylistController()
		self.controller = self.controllers[mode]
		#self.osc_receiver = OSCReceiver()
		self.master_ip = master_ip
		self.previous_position = -1.0
		self.arena_controller = ArenaController()

	@classmethod
	def get_modes(self):
		return modes

	def get_settings(self, format=None):
		return self.controller.get_settings(format)

	def apply_settings(self, settings):
		self.controller.apply_settings(settings)

	def set_mode(self, mode):
		self.mode = mode
		self.controller = self.controllers[self.mode]

	def set_master_ip(self, ip):
		self.master_ip = ip

	def set_arena_controller(self, arena_controller):
		self.arena_controller = arena_controller

	def add_clip(self, clip):
		self.controller.add_clip(clip)

	def update_clip(self, clip):
		self.controller.update_clip(clip)

	def delete_clip(self, clip):
		self.controller.delete_clip(clip)

	def reset(self):
		self.controller.reset()

	def get_clips(self):
		return self.controller.get_clips()

	def _send_next_clip(self):
		clip = self.controller.get_next_clip()
		if self.arena_controller is not None:
			self.arena_controller.set_clip(clip)

	def get_next_clip(self):
		return self.controller.get_next_clip()

	def position_callback(self, values, sender):
		if sender[0] == self.master_ip:
			current_position = values
			if values < self.previous_position:
				self._send_next_clip()
				self.previous_position = -1.0
			else:
				self.previous_position = current_position

