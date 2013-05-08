from nodes import *
from pprint import pprint

definitions = []

def get_definitions(data):
    global definitions
    for tlt in data:
        definitions.append(tlt[1])
    #What goes in the symbol table?

def const_tree(data, root, depth):
    if depth == 0:
        for tlt in data:
            tlt_type = tlt[0]
            tlt_name = tlt[1]
            tlt_description = tlt[2]

            df = Definition(tlt_type, tlt_description)
            setattr(root, tlt_name, df)

            #Iterate through the tld and get all the top level directives by checking whether they are tuples
            for tld in tlt:
                if type(tld) is tuple:
                    const_tree(tld, df, 1)

    elif depth == 1:
        tld_type = data[0]

        if tld_type == 'START':
            start = StartDirective()
            stmt_list = data[1]

            #Add the start directive to the definition
            setattr(root, tld_type, start)

            #Recursive call on the list of statements to add to the start directive
            const_tree(stmt_list, start, 2)
        elif tld_type == 'ACTIONS':
            actions = ActionsDirective()
        elif tld_type == 'FUNCTIONS':
            functions = FunctionsDirective()
        elif tld_type == 'DIALOGUE':
            dialogue = DialogueDirective()

    elif depth == 2:
        if isinstance(root, StartDirective):
            for stmt in data:
                stmt_type = stmt[0]
                stmt_node = StatementNode(stmt_type)
                stmt_node.params = stmt[1:]
                root.stmt_list.append(stmt_node)

                error = stmt_node.validate();
        elif isinstance(root, ActionsDirective):
            pass
        elif isinstance(root, FunctionsDirective):
            pass
        elif isinstance(root, DialogueDirective):
            pass

    return root
