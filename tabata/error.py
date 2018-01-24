class Error(Exception):

	def __init__(self, message):
		self._message = str(message)

	@property
	def message(self):
		return self._message

	def __str__(self):
		return self._message
