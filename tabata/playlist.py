from sox import Transformer


class Playlist(object):

	def __init__(self, path):
		self.path = path
		self.reset()

	def reset(self):
		self.slice_idx = 0
		self.song_idx = 0
		self.song_time = 0

	def get_slice(self, time):
		pass
