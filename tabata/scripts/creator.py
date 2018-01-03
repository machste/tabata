from argparse import ArgumentParser, RawDescriptionHelpFormatter
from inspect import cleandoc

from tabata import Exercise, Sequence, Loop


class StdSequence(Sequence):

	PREPARE_TIME = 5
	CYCLES = 8
	WORK_TIME = 45
	REST_TIME = 15

	def __init__(self):
		super(StdSequence, self).__init__("Standard Tabata")
		# Create the prepare exercise and add it to the sequence
		self.prepare = Exercise("Prepare", self.PREPARE_TIME, "./prepare")
		self.add_block(self.prepare)
		## Create the main loop
		self.main_loop = Loop("Main Loop", self.CYCLES)
		# Create the work exercise and add it to the main loop
		self.work = Exercise("Work", self.WORK_TIME, "./work")
		self.main_loop.add_block(self.work)
		# Create the rest exercise and add it to the main loop
		self.rest = Exercise("Rest", self.REST_TIME, "./rest")
		self.main_loop.add_block(self.rest)
		self.add_block(self.main_loop)


class Creator(object):
	"""Tabata Creator Command Line Tool

	The Tabata Creator helps you putting together and mixing your preferenced
	music for your own Tabata Training.
	"""

	def __init__(self):
		self.root_block = StdSequence()
		self.parser = ArgumentParser(prog="tabata",
				formatter_class=RawDescriptionHelpFormatter,
				description=cleandoc(Creator.__doc__))

	def init_parser(self, parser):
		parser.add_argument("-p", "--prepare-time", type=float, metavar="TIME",
				help="Set the time in seconds before the first work exercise "
				"starts.", default=StdSequence.PREPARE_TIME)
		parser.add_argument("-c", "--cycles", type=int, metavar="N",
				help="Set the number of cycles.", default=StdSequence.CYCLES)
		parser.add_argument("-w", "--work-time", type=float, metavar="TIME",
				help="Set the duration of the work exercise in seconds.",
				default=StdSequence.WORK_TIME)
		parser.add_argument("-r", "--rest-time", type=float, metavar="TIME",
				help="Set the duration of the rest exercise in seconds.",
				default=StdSequence.REST_TIME)

	def parse(self, parser):
		self.args = parser.parse_args()

	def run(self, args):
		self.root_block.prepare.time = args.prepare_time
		self.root_block.main_loop.cycles = args.cycles
		self.root_block.work.time = args.work_time
		self.root_block.rest.time = args.rest_time
		self.root_block.play()

	def start(self):
		self.init_parser(self.parser)
		self.parse(self.parser)
		self.run(self.args)


def main():
	"""Main Program

	This is the entry point for the 'tabata' console script.
	"""
	creator = Creator()
	creator.start()

if __name__ == "__main__":
	main()
