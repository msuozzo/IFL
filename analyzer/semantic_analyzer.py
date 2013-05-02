from nodes import Node, DefinitionNode, StatementNode
from pprint import pprint

# def debug(node, tabs_count = 0):
# 	"""Prints out all of the children of a Node."""
# 	text = ""
# 	tabs = " "
# 	for i in range(tabs_count):
# 		tabs = tabs + "\t"

# 	for n in node.get_children():
# 		if type(n) is Node:
# 			text = text + tabs + debug(n, tabs_count + 1)
# 			text = text + "\n"
# 		elif n is None:
# 			text = text + "\n" + tabs + "None"
# 		else:
# 			text = text + "\n" + tabs + n

# 	return text

def debug(node, tabs_count = 0):
	"""Prints out the type, ID if available, and parameters of a node."""

	# generate the correct number of tabs
	tabs = "\t"
	for i in range(tabs_count):
		tabs = tabs + "\t"

	text = ""

	if hasattr(node, "type"):
		text = text + "Type: " + node.type
		# print text

	if hasattr(node, 'ID'):
		text = text + ", ID: " + node.ID
		# print text

	if isinstance(node, str):
		text = text + "\n" + tabs + node
		# print text

	if node is None:
		text = text + "\n" + tabs + "None"
		# print text

	if type(node) is list:
		for l in node:
			text = text + "\n" + tabs + debug(l, tabs_count + 1)
		# print text

	if hasattr(node, "parameters"):
		for n in node.parameters:

			if n is None:
				text = text + "\n" + tabs + "None"
			elif isinstance(n, str):
				# print "inside if isinstance(n, str)"
				text = text + "\n" + tabs + n
			elif type(node) is DefinitionNode or type(node) is StatementNode:
				# print "inside elif type(node) is DefinitionNode"
				text = text + "\n" + tabs + debug(n, tabs_count + 1)
			else:
				# print "inside of else"
				text = text + "\n" + tabs + debug(n, tabs_count + 1)

	return text




def tree_traversal(node):
	"""Goes through each node and each node's children once"""
	for n in node.get_children():
		if type(n) is Node:
			tree_traversal(n)
		elif n is None:
			pass
		else:
			pass

# def add_definition_node(node):
# 	children = node.get_children()
# 	d = DefinitionNode(children[0], children[2])
# 	node.node_type = d
# 	return node


# def add_statement_node(node):
# 	s = StatementNode(node.children[0])
# 	s.add_parameters(node.children[1:])
# 	node.node_type = s
# 	return node



# def semantic_analyze(node):
# 	children = node.get_children()
# 	if children[0] in ["CHARACTER", "TRAIT", "ITEM", "SETTING"]:
# 		return add_definition_node(node)
# 	else:
# 		return add_statement_node(node)


# def construct_tree(data):
# 	"""Create a tree based on the input from the parser."""
# 	current_parent = Node("parent")

# 	for token in data:
# 		if type(token) is tuple:
# 			n = construct_tree(token)
# 			current_parent.add_child(n)
# 		else:
# 			current_parent.add_child(token)

# 	return semantic_analyze(current_parent)

def construct_tree(data, root=None):
	"""Create a tree based on the input from the parser."""

	# unique case where the root is initially empty
	if root is None:
		current_node = DefinitionNode("ROOT", "root")

		for token in data:
			current_node.add_parameters(construct_tree(token, current_node))

		return current_node

	else:

		if type(data[0]) is tuple:
			current_node = root
			for token in data:
				current_node.add_parameters(construct_tree(token, current_node))
			
			return None

		if (data[0] == "TRAIT" or
			data[0] == "CHARACTER" or
			data[0] == "SETTING" or
			data[0] == "ITEM"):
			current_node = DefinitionNode(data[0], data[1])
			iteration_start = 2
		else:
			current_node = StatementNode(data[0])
			iteration_start = 1

		for token in data[iteration_start:]:

			if type(token) is tuple:
				current_node.add_parameters(construct_tree(token, current_node))
			elif token is None:
				current_node.add_parameters("None")
			else:
				current_node.add_parameters(token)

		return current_node

