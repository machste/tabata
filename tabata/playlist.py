import logging
import os

from sox import Transformer

from tabata.song import Song
from tabata.utils import format_time

_log = logging.getLogger(__name__)


class Playlist(object):

	def __init__(self, name, path, temp_dir):
		self.name = name
		self.path = path
		self.sort_songs = True
		self.temp_dir = temp_dir
		self.begin_guard_time = 10
		self.end_guard_time = 10
		self.fade_in_time = 1
		self.fade_out_time = 1
		self.songs = []
		self.load_songs()
		self.reset()

	def load_songs(self):
		for f in os.listdir(self.path):
			song = Song(os.path.join(self.path, f))
			song.load_infos()
			if song.duration > 0:
				_log.debug("Append '%s' to '%s'" % (song, self.name))
				self.songs.append(song)
		if self.sort_songs:
			self.songs.sort(key=lambda song: song.filepath)

	def reset(self):
		self.slice_idx = 0
		self.song_idx = 0
		self.song_time = 0

	def get_current_song(self):
		return self.songs[self.song_idx]

	def get_slice(self, duration, out_file=None):
		if out_file == None:
			# Generate file name for slice
			file_name = "%s_%i.wav" % (self.name, self.slice_idx)
			out_file = os.path.join(self.temp_dir, file_name)
		# Calculate duration and fade in and out time
		duration += (self.fade_in_time + self.fade_out_time) / 2
		# Apply guard time at the beginning of the song
		if self.song_time < self.begin_guard_time:
			self.song_time = self.begin_guard_time
		# Calculate end time of the slice
		end_time = self.song_time + duration
		# Look for a possible slice
		slice_found = False
		song = self.get_current_song()
		while not slice_found:
			# Check if the current song still has enough time left
			if end_time < song.duration:
				slice_found = True
			else:
				# Skip to next song
				if self.song_idx < len(self.songs) - 1:
					self.song_idx += 1
				elif self.slice_idx <= 0:
					raise Exception("Unable to get slice from playlist!")
				else:
					self.song_idx = 0
				# Calculate new start and end time
				self.song_time = self.begin_guard_time
				end_time = self.song_time + duration
				song = self.get_current_song()
		_log.debug("Slice '%s' %s - %ss" % (song.filepath,
				format_time(self.song_time), format_time(end_time)))
		# Get slice out the song
		slicer = Transformer()
		slicer.trim(self.song_time, end_time)
		slicer.fade(self.fade_in_time, self.fade_out_time)
		slicer.build(song.filepath, out_file)
		_log.debug("Built '%s' (%ss)" % (out_file, format_time(duration)))
		self.song_time = end_time
		self.slice_idx += 1
		# Put together song information and return it
		song = Song(out_file)
		song.duration = duration
		song.fade_in_time = self.fade_in_time
		song.fade_out_time = self.fade_out_time
		return song
