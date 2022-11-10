import json

class ConfigurableComponent:

	def __init__(self):
		self.settings = {}

	def get_settings(self):
		return json.dumps(self.settings)

	def load_settings(self, settings):
		self.settings = json.loads(settings)
		self._apply_settings()