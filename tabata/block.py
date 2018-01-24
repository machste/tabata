import logging
import os

from sox import Combiner

from tabata import global_config
from tabata.song import Song
from tabata.utils import format_time

_log = logging.getLogger(__name__)


class Block(object):

	def __init__(self, name):
		self.name = name

	def build(self, outfile=None):
		raise NotImplementedError

	def play(self):
		song = self.build()
		_log.info("Play: %s" % self)
		song.play()

	def __str__(self):
		return "%s: %s" % (type(self).__name__, self.name)


class Exercise(Block):

	def __init__(self, name, time, playlist):
		super(Exercise, self).__init__(name)
		self.time = float(time)
		self.playlist = playlist

	def build(self, out_file=None):
		return self.playlist.get_slice(self.time, out_file)

	def __str__(self):
		return "%s (%ss from '%s')" % (self.name, format_time(self.time),
				self.playlist.path)


class Sequence(Block):

	def __init__(self, name):
		super(Sequence, self).__init__(name)
		self.blocks = []

	def add_block(self, block):
		if not isinstance(block, Block):
			raise TypeError("%s is not of type 'Block'")
		self.blocks.append(block)

	def build(self, out_file=None):
		if out_file == None:
			# Generate file name for the sequence
			file_name = "%s.wav" % self.name
			temp_dir = global_config.temp_dir
			out_file = os.path.join(temp_dir, file_name)
		songs = []
		# Build all blocks of the sequence
		for block in self.blocks:
			songs.append(block.build())
		# Get song file paths
		in_songs = map(lambda s: s.filepath, songs)
		# Calculate delays
		prev_song = None
		current_delay = 0
		delays = []
		for song in songs:
			if prev_song != None:
				fade_corr = (prev_song.fade_out_time + song.fade_in_time) / 2
				current_delay += prev_song.duration - fade_corr
			# Append calculated delay and remember previous song
			delays.extend([current_delay] * 2)
			prev_song = song
		duration = current_delay + songs[-1].duration
		# Calculate channel remix
		current_channel = 1
		remixes = {1: [], 2: []}
		for i in range(len(songs)):
			remixes[1].append(current_channel)
			remixes[2].append(current_channel + 1)
			current_channel += 2
		# Mix sequence
		mixer = Combiner()
		mixer.delay(delays)
		mixer.remix(remixes)
		mixer.trim(0, duration)
		mixer.build(in_songs, out_file, 'merge')
		# Put together song information and return it
		seq = Song(out_file)
		seq.duration = duration
		seq.fade_in_time = songs[0].fade_in_time
		seq.fade_out_time = songs[-1].fade_out_time
		return seq

class Loop(Sequence):

	def __init__(self, name, cycles):
		super(Loop, self).__init__(name)
		self.cycles = int(cycles)

	def build(self, out_file=None):
		if out_file == None:
			# Generate file name for the loop and the inner sequence
			out_file_name = "%s.wav" % self.name
			seq_file_name = "%s.seq.wav" % self.name
			temp_dir = global_config.temp_dir
			out_file = os.path.join(temp_dir, out_file_name)
			seq_file = os.path.join(temp_dir, seq_file_name)
		# Build inner sequence
		seq = super(Loop, self).build(seq_file)
		# Repeat inner sequence 'cycles'-times as input songs
		in_songs = [seq.filepath] * self.cycles
		# Calculate delays and channel remix
		current_delay = 0
		current_channel = 1
		delays = []
		remixes = {1: [], 2: []}
		for cycle in range(self.cycles):
			if cycle != 0:
				fade_corr = (seq.fade_out_time + seq.fade_in_time) / 2
				current_delay += seq.duration - fade_corr
			# Append calculated delay
			delays.extend([current_delay] * 2)
			# Append current l+r channels to the output l+r channels
			remixes[1].append(current_channel)
			remixes[2].append(current_channel + 1)
			current_channel += 2
		# Calculate the total duration of the loop
		duration = current_delay + seq.duration
		# Mix the loop
		mixer = Combiner()
		mixer.delay(delays)
		mixer.remix(remixes)
		mixer.trim(0, duration)
		mixer.build(in_songs, out_file, 'merge')
		# Put together song information and return it
		loop = Song(out_file)
		loop.duration = duration
		loop.fade_in_time = seq.fade_in_time
		loop.fade_out_time = seq.fade_out_time
		return loop

	def __str__(self):
		return "Loop: %s (%s cycles)" % (self.name, self.cycles)
