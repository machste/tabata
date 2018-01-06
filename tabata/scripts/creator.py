from argparse import ArgumentParser, RawDescriptionHelpFormatter
from inspect import cleandoc

from tabata import global_config
from tabata.block import Exercise, Sequence, Loop
from tabata.playlist import Playlist


class Creator(object):
	"""Tabata Creator Command Line Tool

	The Tabata Creator helps you putting together and mixing your preferenced
	music for your own Tabata Training.
	"""

	def __init__(self):
		self.cfg = global_config
		self.root_block = None
		self.parser = ArgumentParser(prog="tabata",
				formatter_class=RawDescriptionHelpFormatter,
				description=cleandoc(Creator.__doc__))

	def init_parser(self, parser):
		parser.add_argument("-p", "--prepare-time", type=float, metavar="TIME",
				help="Set the time in seconds before the first work exercise "
				"starts.", default=self.cfg.prepare_time)
		parser.add_argument("-c", "--cycles", type=int, metavar="N",
				help="Set the number of cycles.", default=self.cfg.cycles)
		parser.add_argument("-w", "--work-time", type=float, metavar="TIME",
				help="Set the duration of the work exercise in seconds.",
				default=self.cfg.work_time)
		parser.add_argument("-r", "--rest-time", type=float, metavar="TIME",
				help="Set the duration of the rest exercise in seconds.",
				default=self.cfg.rest_time)

	def parse(self, parser):
		# Parse the command line options
		args = parser.parse_args()
		# Put parsed arguments to the tabata configuration
		self.cycles = args.cycles
		self.prepare_time = args.prepare_time
		self.work_time = args.work_time
		self.rest_time = args.rest_time

	def create_std_sequence(self, cfg):
		std_seq = Sequence("Standard Tabata")
		# Create the prepare exercise and add it to the sequence
		prepare = Exercise("Prepare", cfg.prepare_time,
				Playlist(cfg.prepare_path))
		std_seq.add_block(prepare)
		## Create the main loop
		main_loop = Loop("Main Loop", cfg.cycles)
		# Create the work exercise and add it to the main loop
		work = Exercise("Work", cfg.work_time, Playlist(cfg.work_path))
		main_loop.add_block(work)
		# Create the rest exercise and add it to the main loop
		rest = Exercise("Rest", cfg.rest_time, Playlist(cfg.rest_path))
		main_loop.add_block(rest)
		std_seq.add_block(main_loop)
		return std_seq

	def run(self, cfg):
		self.root_block = self.create_std_sequence(cfg)
		self.root_block.play()

	def start(self):
		self.init_parser(self.parser)
		self.parse(self.parser)
		self.run(self.cfg)


def main():
	"""Main Program

	This is the entry point for the 'tabata' console script.
	"""
	creator = Creator()
	creator.start()

if __name__ == "__main__":
	main()
