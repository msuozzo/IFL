from generator_functions import *
import os

def generate_code(node):
    """Select the appropriate function based on the type of the node"""

    if node.func_name == "ADD":
        return generate_add(node.params)

    elif node.func_name == "SET":
        return generate_set(node.params)

    elif node.func_name == "PRINT":
        return generate_print(node.params)


def generate_classes(tree):
    """Traverse through the tree in a DFS format to generate code for classes"""

    # loop through all of the Definition Nodes in the tree
    definition_nodes = dir(tree)
    for element in definition_nodes:
        node = getattr(tree, element)

        #if hasattr(node, "definition_type") and node.ID is not "PLAYER":
        if hasattr(node, "definition_type"):

            # create the file
            file = open("./game/" + node.ID + ".py", 'w')

            # add the appropriate imports by looping through all of the definition nodes
            for element in definition_nodes:
                n = getattr(tree, element)
                if hasattr(n, "definition_type") and node.ID != n.ID :
                    file.write("from %s import *\n" % n.ID)
                    file.write("\n")

            # class declaration begins here
            file.write("class %s:" % node.ID.title() + "\n")

            # iterate through each statement in START and add it to constructor
            file.write("\tdef __init__(self):\n")
            for statement in node.START.stmt_list:

                # get the code, add the appropriate tabs, and write to file
                # (Note that the code might be multi-lined)
                s = generate_code(statement)
                for line in s.splitlines():
                    file.write("\t\t" + line + "\n")

            # create a function to return the description if it has one
            if node.description is not None:
                file.write("\tdef get_description(self):\n")
                file.write("\t\t%s" % node.description)

            # create a list of functions is there is any
            if hasattr(node, "FUNCTIONS"):
                pass

            # create a list of actions if there is any
            if hasattr(node, "ACTIONS"):
                pass

            # create a list of dialogues if there is any
            if hasattr(node, "DIALOGUE"):
                pass

            file.close()

    # end of the for loop here

def generate_game(tree):
    """Generate the main class file for the game"""

    # create the file
    file = open("./game/game.py", 'w')

    # add the appropriate imports by looping through all of the definition nodes
    definition_nodes = dir(tree)
    for element in definition_nodes:
        node = getattr(tree, element)
        if hasattr(node, "definition_type"):
            file.write("from %s import *\n" % node.ID)

    # main body of the game file begins here
    main = """
player = Player()

while True:
    if hasattr(player, "location"):
        print player.location.description

    print "What would you like to do now?"
    print "Enter commands like 'get apple' (action noun):"
    input = raw_input("Enter 'help' for more:")

    if input == "help":
        # loop through all of the actions, items, character in setting and print them out
        print "Hello world!"
    """

    main = main + """
    input = input.split()
    action = input[0]
    if len(input) > 1:
	    noun = input[1]
	    print "action is " + action
	    print "noun is " + noun
	    """


    file.write(main)


    file.close()


def generator(tree):
    """Generate Python code based on the tree that's given"""

    # create the game directory if it does not already exist
    if not os.path.exists("./game"):
        os.mkdir("./game")

    # create the classes for each ITEM, CHARACTER, TRAIT, and SETTING
    generate_classes(tree)

    # create the while and infinite loop that asks the user for inputs
    generate_game(tree)

