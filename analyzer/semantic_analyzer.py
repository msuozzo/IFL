from nodes import *
from pprint import pprint

definitions = {}
error_list = []

def get_definitions(data):
    global definitions
    for tlt in data:
        definitions[tlt[1]] = tlt[0]

class Primitive():
    def __init__(self, params):
        self.ID = params[1]
        self.value = params[2]

class DefinitionObject():
    def __init__(self, params):
        self.ID = params
        self.value = params.capitalize() + "()"
        self.definition_type = definitions[params]

def const_tree(data, root, depth):
    '''
    Keyword Arguments
    '''
    if depth == 0:
        for tlt in data:
            tlt_type = tlt[0]
            tlt_id = tlt[1]
            tlt_description = tlt[2]

            df = Definition(tlt_id, tlt_type, tlt_description)
            setattr(root, tlt_id, df)

            #Iterate through the tld and get all the top level directives by checking whether they are tuples
            for tld in tlt:
                if type(tld) is tuple:
                    const_tree(tld, df, 1)

    elif depth == 1:
        tld_type = data[0]

        if tld_type == 'START':
            start_dir = StartDirective()
            stmt_list = data[1]

            #Add the start directive to the definition
            setattr(root, tld_type, start_dir)

            #Recursive call on the list of statements to add to the start directive
            const_tree(stmt_list, start_dir, 2)

        elif tld_type == 'ACTIONS':
            actions_dir = ActionsDirective()
            func_list = data[1]

            setattr(root, tld_type, actions_dir)
            const_tree(func_list, actions_dir, 2)

        elif tld_type == 'FUNCTIONS':
            func = FunctionsDirective()

        elif tld_type == 'DIALOGUE':
            dialogue = DialogueDirective()

    elif depth == 2:
        if isinstance(root, StartDirective):
            stmt_list = parse_stmt_list(data)
            root.stmt_list = stmt_list

                # error = stmt_node.validate();
                # if error:
                #     errors.append(error)

        elif isinstance(root, ActionsDirective):
            for function in data:
                func_name = function[0]
                stmt_list = parse_stmt_list(function[1])
                root.actions_list[func_name] = stmt_list

        elif isinstance(root, FunctionsDirective):
            pass
        elif isinstance(root, DialogueDirective):
            pass

    return root

def parse_stmt_list(stmt_list):
    stmt_node_list = []
    for stmt in stmt_list:
        stmt_node_list.append(parse_stmt(stmt))

    return stmt_node_list

def parse_stmt(stmt):
    stmt_map = {
        'ADD': parse_add,
        'SET': parse_set,
        'PRINT': parse_print,
        'INCREASE': parse_increase,
        'DECREASE': parse_decrease,
        'MOVE': parse_move,
        'REMOVE': parse_remove,
        'IF': parse_conditional,
    }

    stmt_type = stmt[0]
    stmt_params = stmt[1:]

    params = stmt_map[stmt_type](stmt_params)
    stmt_node = StatementNode(stmt_type, params)

    # error = stmt_node.validate()
    # error_list.append(error)

    return stmt_node

def parse_add(params):
    param_map = {}
    try:
        param_map['quantity'] = params[0]
        if type(params[1]) == tuple:
            param_map['obj'] = Primitive(params[1])
        else:
            param_map['obj'] = DefinitionObject(params[1])
        param_map['target'] = list(params[2])

    except(ValueError):
        pass

    return param_map

def parse_set(params):
    param_map = {}
    try:
        param_map['target'] = list(params[0])
        param_map['value'] = params[1]
    except(ValueError):
        pass

    return param_map

def parse_increase(params):
    pass
def parse_decrease(params):
    pass

def parse_print(params):
    param_map = {}
    param_map['value'] = str(params[0][0])

    return param_map

def parse_move(params):
    pass

def parse_remove(params):
    pass

def parse_conditional(params):
    if_condition = params[0]
    else_condition = params[-1]