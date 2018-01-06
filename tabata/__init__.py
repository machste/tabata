class Config(object):

	def __init__(self):
		# Parameters for the standard sequence 
		self.cycles = 8
		self.prepare_time = 5
		self.prepare_path = "./prepare"
		self.work_time = 45
		self.work_path = "./work"
		self.rest_time = 15
		self.rest_path = "./rest"
		# Parameters for building the tabata
		self.temp_dir = None


global_config = Config()
