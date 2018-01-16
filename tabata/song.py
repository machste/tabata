import logging
import sox

from tabata.utils import format_time

_log = logging.getLogger(__name__)

class Song(object):

	def __init__(self, filepath):
		self.filepath = filepath
		self.duration = 0
		self.fade_in_time = 0
		self.fade_out_time = 0

	def load_infos(self):
		self.duration = sox.file_info.duration(self.filepath)

	def play(self):
		player = sox.Transformer()
		_log.debug("Play '%s'" % self.filepath)
		player.preview(self.filepath)

	def __str__(self):
		return "Song: %s (%ss)" % (self.filepath, format_time(self.duration))
