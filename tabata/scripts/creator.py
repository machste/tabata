import logging

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from inspect import cleandoc

from tabata import global_config
from tabata.block import Exercise, Sequence, Loop
from tabata.playlist import Playlist
from tabata.error import Error

_log = logging.getLogger(__name__)


class Creator(object):
	"""Tabata Creator Command Line Tool

	The Tabata Creator helps you putting together and mixing your preferenced
	music for your own Tabata Training.
	"""

	def __init__(self):
		self.cfg = global_config
		self.playlists = []
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
		parser.add_argument("outfilepath", metavar="OUTFILE", nargs="?",
				help="Define the output file to which the tabata is written. "
				"If no file is defined the tabata will be instantly played.")

	def parse(self, parser):
		# Parse the command line options
		args = parser.parse_args()
		# Put parsed arguments to the tabata configuration
		self.cfg.cycles = args.cycles
		self.cfg.prepare_time = args.prepare_time
		self.cfg.work_time = args.work_time
		self.cfg.rest_time = args.rest_time
		self.cfg.outfilepath = args.outfilepath

	def create_std_sequence(self, cfg):
		# Create needed playlist for prepare, work and rest exercises
		prepare_playlist = Playlist("prepare", cfg.prepare_path, cfg.temp_dir)
		work_playlist = Playlist("work", cfg.work_path, cfg.temp_dir)
		rest_playlist = Playlist("rest", cfg.rest_path, cfg.temp_dir)
		self.playlists.extend([prepare_playlist, work_playlist, rest_playlist])
		# Create the standard tabata sequence
		std_seq = Sequence("standard_tabata")
		# Create the prepare exercise and add it to the sequence
		prepare = Exercise("Prepare", cfg.prepare_time, prepare_playlist)
		std_seq.add_block(prepare)
		## Create the main loop
		main_loop = Loop("main_loop", cfg.cycles)
		# Create the work exercise and add it to the main loop
		work = Exercise("work", cfg.work_time, work_playlist)
		main_loop.add_block(work)
		# Create the rest exercise and add it to the main loop
		rest = Exercise("rest", cfg.rest_time, rest_playlist)
		main_loop.add_block(rest)
		std_seq.add_block(main_loop)
		return std_seq

	def run(self, cfg):
		self.root_block = self.create_std_sequence(cfg)
		_log.info("Play Tabata ...")
		if cfg.outfilepath is None:
			self.root_block.play()
		else:
			self.root_block.build(cfg.outfilepath)

	def cleanup(self):
		self.cfg.cleanup()

	def start(self):
		self.init_parser(self.parser)
		self.parse(self.parser)
		try:
			self.run(self.cfg)
		except KeyboardInterrupt:
			_log.warn("Aborted by user!")
		except Error as e:
			_log.error(e.message)
		finally:
			self.cleanup()


def main():
	"""Main Program

	This is the entry point for the 'tabata' console script.
	"""
	logging.basicConfig()
	creator = Creator()
	creator.start()

if __name__ == "__main__":
	main()
