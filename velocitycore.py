from velocitycontroller import VelocityController
from clipmanager import ClipManager
from arenacontroller import ArenaController
from configurationmanager import ConfigurationManager
from oscreceiver import OSCReceiver

modes = [
	"Playlist",
	"OBD"
]

class VelocityCore:

	def __init__(self):
		self.clip_manager = ClipManager()
		self.arena_controller = ArenaController()
		self.configuration_manager = ConfigurationManager()
		self.velocity_controller = VelocityController(arena_controller=self.arena_controller)
		self.osc_receiver = OSCReceiver()
		self.osc_receiver.add_listener('/composition/selectedclip/transport/position', self.arena_callback)
		self.osc_receiver.add_listener('/activeclip/video/position/values', self.arena_callback)
		self.set_mode(modes[1])
		self.previous_position = -1.0
		self.start()
		self.callback_lock = False
		self._apply_settings(self.configuration_manager.get_last_saved_settings())

	def setup(self):
		pass

	def start(self):
		next_clip = self.clip_manager.get_next_clip()
		self.arena_controller.set_clip(next_clip)

	def arena_callback(self, *values):
		if self.callback_lock:
			return
		self.callback_lock = True
		current_position = values[0]
		if current_position > 0.99:
			self.previous_position = -1.0
			next_clip = self.clip_manager.get_next_clip()
			self.arena_controller.set_clip(next_clip)
		else:
			self.previous_position = current_position
		self.callback_lock = False

	def _get_settings(self):
		"""
		Gather settings from various components and send them to the 
		configuration manager.
		"""
		settings = None
		return settings

	def _apply_settings(self, settings):
		"""
		Apply settings from configuration manager to various components.
		"""
		self.clip_manager.apply_settings(settings['clips'])
		self.arena_controller.apply_settings(settings['arena'])
		self.velocity_controller.apply_settings(settings['velocity'])
		self.set_mode(settings['mode'])

	def load_config(self, config):
		"""
		Get settings from configuration manager and apply them.
		"""
		settings = self.configuration_manager.load(config)
		self._apply_settings(settings)

	def save_config(self, name):
		"""
		Save the current running parameters of the application as a configurations
		"""
		#settings = self._get_settings()
		#self.configuration_manager.save(config, settings)
		arena_settings = self.arena_controller.get_settings()
		clip_settings = self.clip_manager.get_settings()
		settings = {}
		settings['mode'] = self.current_mode
		settings['clips'] = clip_settings['clips']
		settings['arena'] = arena_settings
		settings['velocity'] = self.velocity_controller.get_current_config()
		#print(settings)
		self.configuration_manager.save(name, settings)

	def new_config(self):
		"""
		Reset all components.
		"""
		self.clip_manager.reset()
		self.arena_controller.reset()

	def get_configs(self):
		"""
		Return list of saved configs.
		"""
		pass

	def get_current_config(self, format):
		"""
		Dump current settings as raw data or json.
		"""
		pass

	def set_mode(self, mode):
		"""
		Set the input mode. Current options are Playlist and OBD.
		"""
		self.current_mode = mode
		if(self.current_mode == 'OBD'):
			self.callback_lock = True
		else:
			self.callback_lock = False
		print("Set mode to {}".format(self.current_mode))

	def add_clip(self, clip=None):
		"""
		Add a clip to the clip manager. Clip object will contain it's mode along with the 
		required parameters for that mode.
		"""
		self.clip_manager.add_clip(clip)

	def remove_clip(self, clip):
		"""
		Remove a clip.
		"""
		self.clip_manager.remove_clip(clip)

	def update_clip(self, clip):
		"""
		Update parameters of a particular clip. May only apply to certain clip modes. 
		"""
		self.clip_manager.update_clip(clip)

	def delete_clip(self, clip):
		"""
		Update parameters of a particular clip. May only apply to certain clip modes. 
		"""
		self.clip_manager.delete_clip(clip)

	def add_arena_instance(self):
		"""
		Add arena instance to controller.
		"""
		self.arena_controller.add_arena_instance()
		self.start()

	def remove_arena_instance(self, arena_instance):
		"""
		Remove arena instance from controller.
		"""
		self.arena_controller.remove_arena_instance(arena_instance)
		self.start()

	def update_arena_instance(self, instance):
		"""
		Update arena instance IP or master status
		"""
		self.arena_controller.update_arena_instance(instance)
		self.start()

	def get_status(self):
		"""
		Return status of all components.
		"""
		status = {}
		status['breaks'] = self.velocity_controller.get_current_config()['breaks']
		status['configs'] = self.configuration_manager.get_configs()
		status['modes'] = modes
		status['current_mode'] = self.current_mode
		status['clips'] = self.clip_manager.get_clips()
		#status['arena_instances'] = [{'id':0, 'ip':'localhost'},{'id':1, 'ip':'192.168.0.100'},{'id':2, 'ip':'192.168.0.102'}]
		status['arena_instances'] = self.arena_controller.get_arena_instances()
		return status

	def play(self):
		self.velocity_controller.play()

	def pause(self):
		self.velocity_controller.pause()

	def add_range(self):
		self.velocity_controller.add_range()

	def remove_range(self, num):
		self.velocity_controller.remove_range(num)

	def set_playback_speed(self, speed):
		self.velocity_controller.set_playback_speed(speed)

	def update_range(self, b_id, clip, start, stop):
		self.velocity_controller.update_range(b_id, clip, start, stop)

	def get_speed(self):
		#print(self.velocity_controller.get_speed())
		return self.velocity_controller.get_speed()

	def set_arena_version(self, version):
		self.arena_controller.set_version(version)