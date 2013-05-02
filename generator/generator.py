from Trait import Trait
from Character import Character
import re
from pprint import pprint

# def debug(node, tabs_count = 0):
# 	Replace

# 	return text


# def code_generator(node):
# 	if node.get_children()[0] == "":
# 		return trait_generator(node)

def traverse_tree(file, tree):
	"""Traverse through the tree in a DFS format to generate code"""

	for node in tree.get_children():
		pass



def main():

    # set up the header
    file = open("output.py", 'w')

    # cleanse input from the tree
    data = open("tree1.txt").read()
    data = re.split("(\(|\)|,+\s)", data)
    data = filter(lambda a: a != ", ", data) 
    data = filter(lambda a: a != "", data)

    for i in data:
    	print "*" + i + "*"

    tree = construct_tree(data)

    print "The tree is: "
    print debug(tree)

    # in progress
    if isinstance(xx, DefinitionNode):
    	if xx.type == "TRAIT":
    		xx.id = Trait()


    else: # statement node in this case

    #traverse_tree(file, tree)

#   health = Trait()
#	health.setValue('current', 50)

#	health.setValue('current', 100)

#	player = Character()
#	player.setValue("health", health)

# 	print "Hello, I am a character"

if __name__ == '__main__':
    main()















