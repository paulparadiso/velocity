import json
import copy
from itertools import filterfalse
import os
import glob
from obdcontroller import OBDController
import threading
import time

DEFAULT_DIR = 'configs'

BLANK_CONFIG = {
	'params': [],
	'breaks':[]
} 

##
#
# {'clip': 0, 'start': 0, 'end'}
#
##

class VelocityController:

	def __init__(self, save_dir=DEFAULT_DIR, arena_controller=None):
		self.save_dir = save_dir
		self.current_config_name = ''
		self.saved = True
		self._load_default()
		self.obd_controller = OBDController()
		self.arena_controller = arena_controller
		self.current_clip = 0
		self.current_speed = 0
		self.poller = None
		if self.obd_controller.connection != None:
			self._start_polling()

	def _load(self, filename):
		pass

	def _load_default(self):
		self.current_config = copy.copy(BLANK_CONFIG)
		self.add_range(0, 10, 0)
		self.add_range(11, 20, 1)
		self.add_range(21, 30, 2)
		self.add_range(31, 40, 3)
		self.current_config_name = 'Default'

	def _save(self, filename):
		pass

	def _get_last_clip(self):
		last_clip = 0
		for item in self.current_config['breaks']:
			if item['clip'] > last_clip:
				last_clip = item['clip']
		return last_clip

	def _get_last_speed(self):
		last_speed = 0
		for item in self.current_config['breaks']:
			if item['stop'] > last_speed:
				last_speed = item['stop']
		return last_speed

	def _get_last_id(self):
		b_id = -1
		for item in self.current_config['breaks']:
			if item['id'] > b_id:
				b_id = item['id']
		return b_id

	def get_saved(self):
		return self.saved

	def get_current_config(self, format=''):
		if(format == 'json'):
			return json.dumps(self.current_config)
		else:
			return self.current_config

	def get_current_config_name(self):
		return self.current_config_name

	def get_all_configs(self):
		current_dir = os.getcwd()
		configs = []
		path = '{0}/{1}/*.json'.format(current_dir, self.save_dir)
		for file in glob.glob(path):
			configs.append(os.path.basename(file).split('.')[0])
		return configs

	def save_config(self, name):
		filename = '{0}/{1}.json'.format(os.getcwd() + '/' + self.save_dir, name)
		with open(filename, 'w') as outfile:
			json.dump(self.current_config, outfile)
		self.saved = True
		self.load_config(name)

	def apply_settings(self, settings):
		self.current_config = settings

	def load_config(self, name):
		filename = '{0}/{1}.json'.format(os.getcwd() + '/' + self.save_dir, name)
		print('loading - {0}'.format(filename))
		with open(filename, 'r') as infile:
			self.current_config = json.load(infile)
		self.current_config_name = name

	def new_config(self):
		self.current_config['breaks'] = []
		self.add_range(0, 10, 0)
		self.current_config_name = 'Untitled'
		self.saved = False

	def add_range(self, start=None, stop=None, clip=None):
		next_id = self._get_last_id() + 1
		next_clip = self._get_last_clip() + 1
		next_start = self._get_last_speed() + 1
		next_stop = next_start + 9
		self.current_config['breaks'].append({'id': next_id, 'clip': next_clip, 'start': next_start, 'stop': next_stop})

	def remove_range(self, num):
		for item in self.current_config['breaks']:
			if item['id'] == num:
				self.current_config['breaks'].remove(item)
		self.saved = False

	def update_range(self, num, clip, start, stop):
		for item in self.current_config['breaks']:
			if item['id'] == int(num):
				item['clip'] = int(clip)
				item['start'] = int(start)
				item['stop'] = int(stop)
		self.saved = False

	def set_clip(self, clip):
		self.arena_controller.set_clip(clip) 

	def _start_polling(self):
		self.poller = threading.Thread(target=self.poll_obd, daemon=True)
		self.poller.start()

	def _stop_polling(self):
		if self.poller is not None:
			self.poller.stop()

	def poll_obd(self):
		while(True):
			speed = self.obd_controller.get_speed()
			#print(speed)
			self.current_speed = speed
			for b in self.current_config['breaks']:
				#print('Testing {0} against {1} and {2}'.format(speed, b['start'], b['stop']))
				if (speed >= b['start']) and (speed <= b['stop']):
					if b['clip'] != self.current_clip:
						print('Setting clip to {0}'.format(b['clip']))
						self.current_clip = b['clip']
						self.set_clip(self.current_clip)
			time.sleep(0.1)

	def get_speed(self):
		return self.current_speed

	def get_current_clip(self):
		return self.current_clip

	def play(self):
		self.arena_controller.play()

	def pause(self):
		self.arena_controller.pause()

	def set_playback_speed(self, speed):
		playback_speed = float(speed) / 10.0
		self.arena_controller.set_playback_speed(playback_speed)

	def get_arena_version(self):
		return self.arena_controller.get_arena_version()

	def set_arena_version(self, arena_version):
		self.arena_controller.set_arena_version(arena_version)