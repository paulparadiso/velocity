import json
import os
import glob

DEFAULT_DIR = 'configs'

BLANK_CONFIG = {
	'params': [],
	'breaks':[]
} 

defaults_file = 'defaults'

class ConfigurationManager:

	def __init__(self):
		self.save_dir = DEFAULT_DIR
		self.defaults = {}
		self._load_defaults()

	def load(self, name):
		current_config = None
		filename = '{0}/{1}.json'.format(os.getcwd() + '/' + self.save_dir, name)
		#print('loading - {0}'.format(filename))
		with open(filename, 'r') as infile:
			current_config = json.load(infile)
		#print(self.current_config)
		#self.current_config_name = name
		self.defaults['last_saved'] = name
		self._save_defaults()
		return current_config

	def save(self, name, current_config):
		filename = '{0}/{1}.json'.format(os.getcwd() + '/' + self.save_dir, name)
		with open(filename, 'w') as outfile:
			json.dump(current_config, outfile)
		self.defaults['last_saved'] = name
		self._save_defaults()
		#self.saved = True
		#self.load_config(name)

	def _save_defaults(self):
		filename = '{0}/{1}.json'.format(os.getcwd() + '/' + self.save_dir, defaults_file)
		with open(filename, 'w') as outfile:
			json.dump(self.defaults, outfile)

	def _load_defaults(self):
		filename = '{0}/{1}.json'.format(os.getcwd() + '/' + self.save_dir, defaults_file)
		with open(filename, 'r') as infile:
			self.defaults = json.load(infile)

	def get_last_saved_settings(self):
		return self.load(self.defaults['last_saved'])

	def get_configs(self):
		current_dir = os.getcwd()
		configs = []
		path = '{0}/{1}/*.json'.format(current_dir, self.save_dir)
		for file in glob.glob(path):
			name = os.path.basename(file).split('.')[0]
			if name != defaults_file:
				configs.append(name)
		return configs