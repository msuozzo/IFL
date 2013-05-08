from errors import errors

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
        pass

class FunctionsDirective():
    def __init__(self):
        pass

class DialogueDirective():
    def __init__(self):
        pass

class StatementNode():
    def __init__(self, method):
        self.method = method
        self.params = []

    def evaulate_chain(obj):
        pass

    def validate_add(self):
        #Adding a primitive
        if len(self.params) == 3:
            if (self.params[0]):
                error = errors["quantity_primitive"]
            primitive = self.params[1]

        return error
    validate_map = {
        "ADD": validate_add
    }

    def validate(self):
        error = validate_map[self.type]
        return error


