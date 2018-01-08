import logging

from sox import Transformer

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
		player = Transformer()
		audio_file = self.build()
		_log.info(self)
		player.preview(audio_file)

	def __str__(self):
		return "Exercise: %s (%s s from '%s')" % (self.name, self.time,
				self.playlist.path)


class Sequence(Block):

	def __init__(self, name):
		super(Sequence, self).__init__(name)
		self.blocks = []

	def add_block(self, block):
		if not isinstance(block, Block):
			raise TypeError("%s is not of type 'Block'")
		self.blocks.append(block)

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
