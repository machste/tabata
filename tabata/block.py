import logging

from tabata.utils import format_time

_log = logging.getLogger(__name__)


class Block(object):

	def __init__(self, name):
		self.name = name

	def build(self):
		raise NotImplementedError

	def play(self):
		raise NotImplementedError

	def __str__(self):
		return "%s: %s" % (type(self).__name__, self.name)


class Exercise(Block):

	def __init__(self, name, time, playlist):
		super(Exercise, self).__init__(name)
		self.time = float(time)
		self.playlist = playlist

	def build(self):
		return self.playlist.get_slice(self.time)

	def play(self):
		song = self.build()
		_log.info("Play: %s" % self)
		song.play()

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

	def build(self):
		slices = []
		for block in self.blocks:
			block.build()

	def play(self):
		for block in self.blocks:
			block.play()


class Loop(Sequence):

	def __init__(self, name, cycles):
		super(Loop, self).__init__(name)
		self.cycles = int(cycles)

	def play(self):
		for i in range(self.cycles):
			super(Loop, self).play()

	def __str__(self):
		return "Loop: %s (%s cycles)" % (self.name, self.cycles)
