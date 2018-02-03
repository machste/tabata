from tempfile import mkdtemp
from shutil import rmtree


class Config(object):

	def __init__(self):
		self.app_name = "tabata"
		# Parameters for the standard sequence 
		self.cycles = 8
		self.prepare_time = 5
		self.prepare_path = "./prepare"
		self.work_time = 45
		self.work_path = "./work"
		self.rest_time = 15
		self.rest_path = "./rest"
		# Parameters for building the tabata
		self._temp_dir = None
		self.outfilepath = None

	@property
	def temp_dir(self):
		if self._temp_dir is None:
			self._temp_dir = mkdtemp(self.app_name)
		return self._temp_dir

	def cleanup(self):
		if self._temp_dir is not None:
			rmtree(self._temp_dir)

global_config = Config()
