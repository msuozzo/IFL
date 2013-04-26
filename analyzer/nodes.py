class Node(object):
	def __init__(self, data):
		self.data = data
		self.children = []

	def add_child(self, object):
		self.children.append(object)

	def add_child_front(self, object):
		self.children.insert(0, object)

	def get_children(self):
		return self.children

class DefinitionNode(object):
	""" Possible DefinitionNodes include:
		trait_definitions
		character_definitions
		setting_definitions
		item_definitions

		DefinitionNodes must contain a type
		TRAIT/CHARACTER/SETTING/ITEM along with an ID
	"""
	def __init__(self, type, ID):
		self.type = type
		self.ID = ID
		self.parameters = []
		# self.description = []
		# self.start = []
		# self.functions = []
		# self.actions = []
		# self.dialogues = []
		print "***DefintionNode " + type + " is created***"

	def add_parameters(self, parameter):
		self.parameters.append(parameter)

#Increase health on player by 100
class StatementNode(object):
	"""StatementNode"""
	def __init__(self, type):
		self.type = type
		self.parameters = []
		print "***StatementNode " + type + " is created***"

	def add_parameters(self, parameter):
		self.parameters.append(parameter)

	def validate(self):
		pass
		# if type == "print":
		# 	if (args.type != string)
		# 		print "error"

	def evaulate_chain(obj):
		pass
