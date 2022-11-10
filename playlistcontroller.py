from inputcontroller import InputController
import json

class PlaylistController(InputController):

	def __init__(self, clips=None):
		super().__init__(self)

	def reset(self):
		self.clips = []
		self.clips.append({'id': 0, 'num':1})

	def get_settings(self, format=None):
		settings = {}
		settings['clips'] = []
		for clip in self.clips:
			settings['clips'].append({'id': clip['id'], 'num': clip['num']})
		return settings

	def apply_settings(self, clips):
		self.clips = []
		for c in clips:
			self.clips.append({'id': c['id'], 'num': c['num']})

	def add_clip(self, clip):
		if clip == None:
			if len(self.clips) == 0:
				self.clips.append({'id':0, 'num': 1})
			else:
				last_clip = self.clips[-1]
				self.clips.append({'id': last_clip['id'] + 1, 'num': last_clip['num'] + 1})
		else:
			self.clips.append(clip)

	def update_clip(self, clip):
		print(clip)
		for c in self.clips:
			if c['id'] == int(clip['id']):
				c['num'] = int(clip['num'])
		
	def delete_clip(self, clip):
		for c in self.clips:
			if c['id'] == int(clip):
				self.clips.remove(c)

	def remove_clip(self, clip):
		for c in self.clips:
			if c['id'] == clip['id']:
				self.clips.remove(c)

	def get_next_clip(self):
		r = 1
		#print("Next clip = {}".format(self.next_clip))
		if self.clips is not None and len(self.clips) > 0:
			r = self.clips[self.next_clip]['num']
			self.next_clip = (self.next_clip + 1) % len(self.clips)
		return r