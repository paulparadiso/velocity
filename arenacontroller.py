from oscpy.client import OSCClient
from configurablecomponent import ConfigurableComponent
import json

osc_messages = {
	'4':{
		'set_clip':'/layer1/clip{0}/connect',
		'set_playback_speed':'/activeclip/video/position/speed',
		'play_pause':'/activeclip/video/position/direction'
	},
	'5':{
		'set_clip':'/layer1/clip{0}/connect',
		'set_playback_speed':'/activeclip/video/position/speed',
		'play_pause':'/activeclip/video/position/direction'
	},
	'6':{
		'set_clip':'/composition/layers/1/clips/{0}/connect',
		'set_playback_speed':'/composition/selectedclip/transport/position/behaviour/speed',
		'play_pause':'/composition/selectedclip/transport/position/behaviour/playdirection'
	}
}

class ArenaInstance:

	def __init__(self, name, address, port=7000, arena_version='6', is_master=False):
		self.name = name
		self.address = address 
		self.port = port
		self.osc = OSCClient(self.address, self.port)
		self.arena_version = arena_version
	
	def get_name(self):
		return self.name

	def get_address(self):
		return self.address

	def get_version(self):
		return self.arena_version

	def set_version(self, version):
		self.arena_version = version

	def update(self, settings):
		print("Updating {} to {}".format(self.name, settings['ip']))
		self.address = settings['ip']
		self.osc = OSCClient(self.address, self.port)
		print(type(settings['arena_version']))
		self.arena_version = settings['arena_version']
		if self.arena_version not in osc_messages.keys():
			self.arena_version = '6'

	def send_message(self, address, values = [0]):
		#print("Sending values {}".format(values))
		msg = osc_messages[self.arena_version][address].format(int(values[0]))
		print("Sending - {} to {}".format(msg, self.address))
		self.osc.send_message(str.encode(msg), values)

class ArenaController(ConfigurableComponent):

	def __init__(self):
		super().__init__()
		self.settings['arena_instances'] = []
		self.settings['master_instance'] = None
		#self.settings['arena_instances'] = self.arena_instances
		#self.master_instance = 
		self.arena_instances = self.settings['arena_instances']
		self.master_instance = self.settings['master_instance']

	def _set_master(self, id):
		print("Setting {} as master".format(id))
		self.master_instance = int(id)

	def get_master_ip(self):
		for instance in self.arena_instances:
			if instance.get_name() == self.master_instance:
				if instance.get_address() == '0.0.0.0':
					return '127.0.0.1'
				else:
					return instance.get_address()
		return None

	#def _apply_settings():
	#	pass

	def get_settings(self, format=None):
		settings = {}
		settings['master_instance'] = self.master_instance
		settings['arena_instances'] = []
		for instance in self.arena_instances:
			settings['arena_instances'].append({'id': instance.get_name(), 'ip': instance.get_address(), 'arena_version': instance.get_version()})
		if format == 'json':
			return json.dumps(settings)
		else:
			return settings

	def apply_settings(self, settings):
		self.arena_instances = []
		self.master_instance = None
		for instance in settings['arena_instances']:
			self.arena_instances.append(ArenaInstance(instance['id'],
													  instance['ip'],
													  port=7000,
													  arena_version=instance['arena_version']))
		self.master_instance = settings['master_instance']
		print('instances - {}, master - {}'.format(self.arena_instances, self.master_instance))

	def add_arena_instance(self, name=None, address=None, port=7000, arena_version='6'):
		name = 0
		if len(self.arena_instances) > 0:
			name = self.arena_instances[-1].get_name() + 1
		is_master = False
		if address == None:
			arena_instance_address = '127.0.0.1'
		else:
			arena_instance_address = address
		self.arena_instances.append(ArenaInstance(name, arena_instance_address, port, arena_version, is_master))
		if len(self.arena_instances) == 1:
			self._set_master(name)

	def update_arena_instance(self, arena_instance):
		for instance_iter in self.arena_instances:
			if instance_iter.get_name() == int(arena_instance['id']):
				instance_iter.update(arena_instance)
		if arena_instance['is_master']:
			self._set_master(arena_instance['id'])

	def remove_arena_instance(self, name):
		try:
			del self.instances[name]
		except KeyError:
			return

	def get_arena_instances(self):
		instances = []
		for instance_iter in self.arena_instances:
			is_master = False
			if instance_iter.get_name() == self.master_instance:
				is_master = True
			instances.append({'id': instance_iter.get_name(), 
							  'ip': instance_iter.get_address(), 
							  'is_master': is_master,
							  'arena_version': instance_iter.get_version()})
		#print(instances)
		return instances

	def _send(self, address, values = [0]):
		for name, instance in self.arena_instances.items():
			instance.send_message(str.encode(address), values)

	def reset(self):
		self.arena_instances = []
		self.arena_instances.append(ArenaInstance(0, '0.0.0.0', 7000, '6'))
		self.master_instance = 0

	def play(self, reverse=False):
		dir = 1
		if reverse:
			dir = 0
		#self._send(b'/composition/selectedclip/transport/position/behaviour/playdirection', [dir])
		#self._send(b'/activeclip/video/position/direction', [dir])
		#address = osc_messages[self.arena_version]['play_pause']
		#self._send(str.encode(address), [dir])
		for instance in self.arena_instances:
			#print("Sending {} to {}".format(clip_num, instance.get_address()))
			instance.send_message('play_pause', [dir])

	def pause(self):
		#self._send(b'/composition/selectedclip/transport/position/behaviour/playdirection', [2])
		#self._send(b'/activeclip/video/position/direction', [2])
		#address = osc_messages[self.arena_version]['play_pause']
		#self._send(str.encode(address), [2])
		for instance in self.arena_instances:
			#print("Sending {} to {}".format(clip_num, instance.get_address()))
			instance.send_message('play_pause', [2])

	def set_clip(self, clip_num):
		#address = '/composition/layers/1/clips/{0}/connect'.format(int(clip_num))
		#address = '/layer1/clip{0}/connect'.format(int(clip_num))
		#address = osc_messages[self.arena_version]['set_clip'].format(int(clip_num))
		#self._send(str.encode(address), [1])
		for instance in self.arena_instances:
			#print("Sending {} to {}".format(clip_num, instance.get_address()))
			instance.send_message('set_clip', [clip_num])

	def set_playback_speed(self, pct):
		#self._send(b'/composition/selectedclip/transport/position/behaviour/speed', [float(pct)])
		#self._send(b'/activeclip/video/position/speed', [float(pct)])
		#address = osc_messages[self.arena_version]['set_playback_speed']
		#self._send(str.encode(address), [float(pct)])
		print('{}'.format(self.arena_instances))
		for instance in self.arena_instances:
			print('sending speed - {}, to {}'.format(pct, instance.get_address()))
			#print("Sending {} to {}".format(clip_num, instance.get_address()))
			instance.send_message('set_playback_speed', [float(pct)])
