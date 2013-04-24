class Character:

	def __init__(self):
		self.d = dict();

	def setValue(self, key, value):
		self.d[key] = value

	def getValue(self, key):
		return self.d[key]

