import logging
import os

from sox import Transformer

_log = logging.getLogger(__name__)


class Playlist(object):

	def __init__(self, name, path, temp_dir):
		self.name = name
		self.path = path
		self.temp_dir = temp_dir
		self.songs = []
		self.load_songs()
		self.reset()

	def load_songs(self):
		for f in os.listdir(self.path):
			song_file = os.path.join(self.path, f)
			if os.path.isfile(song_file):
				_log.debug("Append '%s' to '%s'" % (song_file, self.name))
				self.songs.append(song_file)

	def reset(self):
		self.slice_idx = 0
		self.song_idx = 0
		self.song_time = 0

	def get_slice(self, time):
		file_name = "%s_%i.wav" % (self.name, self.slice_idx)
		out_file = os.path.join(self.temp_dir, file_name)
		slicer = Transformer()
		slicer.trim(self.song_time, self.song_time + time)
		slicer.fade(fade_in_len=2, fade_out_len=2)
		slicer.build(self.songs[self.song_idx], out_file)
		_log.debug("Built '%s' (%is)" % (out_file, time))
		self.song_time += time
		self.slice_idx += 1
		return out_file
