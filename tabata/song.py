import sox

from tabata.utils import format_time


class Song(object):

	def __init__(self, filepath):
		self.filepath = filepath
		self.load_infos()

	def load_infos(self):
		
		self.duration = sox.file_info.duration(self.filepath)

	def __str__(self):
		return "Song: %s (%ss)" % (self.filepath, format_time(self.duration))
