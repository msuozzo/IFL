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
	"""
	def __init__(self, type, description):
		self.type = type
		self.description = description
		self.start = []
		self.functions = []
		self.actions = []
		self.dialogues = []

#Increase health on player by 100
class StatementNode(object):
	"""StatementNode"""
	def __init__(self, type):
		self.type = type

	def add_parameters(self, args):
		self.parameters = args

	def validate(self):
		pass
		# if type == "print":
		# 	if (args.type != string)
		# 		print "error"

	def evaulate_chain(obj):
		pass
