from parser.ifl import generate_lexer
from parser.ifl_yacc import generate_parser
from parser.preprocessor import clean_input

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
		else:
			text = text + "\n" + tabs + n

	return text

def construct_tree(data):
	"""Create a tree based on the input from the parser."""
	current_parent = Node("parent")

	for token in data:
		if type(token) is tuple:
			n = construct_tree(token)
			current_parent.add_child(n)
		else:
			current_parent.add_child(token)

	return current_parent

lexer, tokens = generate_lexer()

parser = generate_parser(lexer, tokens)
data = open("examples/ex1.ifl").read()
cleaned_data = '\n'.join(clean_input(data))

lexer.input(cleaned_data)

while True:
    tok = lexer.token()
    if not tok: break
    print tok

tree = parser.parse(cleaned_data)

t = construct_tree(tree)

for a in t.get_children():
	for b in a.get_children():
		print b
	print "\n"




















