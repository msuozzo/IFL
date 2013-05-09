import os

def generate_code(node):
    # if node.method == "ADD":
    #     return generate_add(node.params)
    #
    # elif node.method == "SET":
    #     return generate_set(node.params)
    #
    # elif node.method == "PRINT":
    #     return generate_print(node.params)
    return "pass\n"



def generate_classes(tree):
    """Traverse through the tree in a DFS format to generate code for classes"""

    definition_nodes = dir(tree)

    for element in definition_nodes:
        node = getattr(tree, element)

        if hasattr(node, "definition_type") and node.ID is not "PLAYER":

            # create the file
            file = open("./game/" + node.ID + ".py", 'w')

            # write the first line
            file.write("class %s:" % node.ID.title() + "\n")

            # iterate through each statement in START and add it to constructor
            file.write("\tdef __init__(self):\n")
            for statement in node.START.stmt_list:

                s = generate_code(statement)

                # get the code, add the appropriate tabs, and write to file
                # (Note that the code might be multi-lined)
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

def generate_game(tree):
    """Generate the main class file for the game"""

    # create the file
    file = open("./game/game.py", 'w')

    # add the appropriate imports by looping through all of the definition nodes
    definition_nodes = dir(tree)

    for element in definition_nodes:
        node = getattr(tree, element)
        if hasattr(node, "definition_type"):
            file.write("import %s\n" % node.ID)

    file.write("\n")




    file.write("player = Player()\n")
    file.write("while true:\n")
    file.write("\tinput = raw__input('What would you like to do now?')")
    file.close()


def generator(tree):
    if not os.path.exists("./game"):
        os.mkdir("./game")

    """Generate Python code based on the tree that's given"""
    generate_classes(tree)

    # create the while and infinite loop that asks the user for inputs
    generate_game(tree)

