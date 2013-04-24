from nodes import Node, DefinitionNode, StatementNode

def debug(node, tabs_count = 0):
	"""Prints out all of the children of a Node."""
	text = ""
	tabs = " "
	for i in range(tabs_count):
		tabs = tabs + "\t"

	for n in node.get_children():
		if type(n) is Node:
			text = text + tabs + debug(n, tabs_count + 1)
			text = text + "\n"
		elif n is None:
			text = text + "\n" + tabs + "None"
		else:
			text = text + "\n" + tabs + n

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

def add_definition_node(node):
	children = node.get_children()
	d = DefinitionNode(children[0], children[2])
	node.node_type = d
	return node


def add_statement_node(node):
	s = StatementNode(node.children[0])
	s.add_parameters(node.children[1:])
	node.node_type = s
	return node



def semantic_analyze(node):
	children = node.get_children()
	if children[0] in ["CHARACTER", "TRAIT", "ITEM", "SETTING"]:
		return add_definition_node(node)
	else:
		return add_statement_node(node)



def construct_tree(data):
	"""Create a tree based on the input from the parser."""
	current_parent = Node("parent")

	for token in data:
		if type(token) is tuple:
			n = construct_tree(token)
			current_parent.add_child(n)
		else:
			current_parent.add_child(token)

	return semantic_analyze(current_parent)











