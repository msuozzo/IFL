from validate import *

class Program():
    def __init__(self):
        pass

class Definition():
    """ Possible DefinitionNodes include:
        trait_definitions
        character_definitions
        setting_definitions
        item_definitions

        DefinitionNodes must contain a type
        TRAIT/CHARACTER/SETTING/ITEM along with an ID
    """
    def __init__(self, ID, definition_type, description):
        self.ID = ID
        self.definition_type = definition_type
        self.description = description

    def __str__(self):
        return "Definition Node - Type: " + self.type + " ID: " + self.ID

class StartDirective():
    def __init__(self):
        self.stmt_list = []

class ActionsDirective():
    def __init__(self):
        self.actions_list = {}

class FunctionsDirective():
    def __init__(self):
        pass

class DialogueDirective():
    def __init__(self):
        pass

class FunctionNode():
    def __init__(self, func_name, params, stmt_list):
        self.func_name = func_name
        self.params = params
        self.stmt_list = []

class StatementNode():
    def __init__(self, func_name, params):
        self.func_name = func_name
        self.params = params

    def evaulate_chain(obj):
        pass

    def validate(self):
        error_msg = validate_map[self.func_name](self.params)
        return error(str(self), error_msg)

    def __str__(self):
        return self.func_name + str(self.params)

class error():
    def __init__(self, line, error_msg):
        self.line = line
        self.error_msg = error_msg

