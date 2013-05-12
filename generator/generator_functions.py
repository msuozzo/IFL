#TODO location remove
#TODO String concatenation
#TODO comments

class FunctionGenerator():
    def __init__(self, id_, tree):
        self.id_ = id_
        self.tree = tree

    def get_type(self, id_):
        try:
            return self.tree.def_types[id_]
        except KeyError:
            return None

    #settings[player.location].characters[%s] %last
    def resolve_target(self, target_list):
        target_list = list(target_list)

        if target_list[0] == 'LIT':
            return target_list[1]
        if target_list[0] == 'OBJ': #It is an object chain, strip out the first word
            target_list = target_list[1:]
        if target_list[0] == self.id_ or target_list[0] == 'SELF':
            target_list[0] = 'self'
        elif target_list[0] == 'PLAYER':
            target_list[0] = 'player'
        elif self.get_type(target_list[0]) == 'CHARACTER':
            target_list[0] = "settings[player.location].characters['%s']" %target_list[0]
        elif target_list[0] == 'LOCATION':
            target_list[0] = 'settings[player.location]'
        target_string = '.'.join(target_list)
        return target_string

    def generate_has(self, node):
        holdee = node[2]
        holder = self.resolve_target(node[1])

        if self.get_type(holdee) == 'ITEM':
            return_stmt = "'{holdee}' in {holder}.items and {holder}.items['{holdee}'][1] > 0".format(holder=holder, holdee=holdee)
        else:
            return_stmt = "hasattr({holder}, {holdee})".format(holder=holder, holdee=holdee)

        return '(' + return_stmt + ')'

    def generate_print(self, node):
        return "print \"" + node.string_expr + "\"\n"

    #TODO test if add and set work for strings and decimals, differentiate between strings and ints
    def generate_add(self, node):
        target = self.resolve_target(node.to)

        if node.primitive:
            attr = node.primitive.name
            if node.primitive.type_ == 'STRING':
                val = "'" + node.primitive.val[0] + "'"
            else:
                val = node.primitive.val[1]
            return_stmt = "{target}.{attr} = {value}".format(target=target, attr=attr, value=val)
        elif self.get_type(node.id_) == 'ITEM':
            original_count = "{target}.items['{id_}'][1]".format(target=target, id_=node.id_)
            new_thing = node.id_.capitalize() + "()"
            return_stmt =\
                "if '{id_}' in {target}.items:\n" \
                    "\t{target}.items['{id_}'][1] = {original_count} + {quantity}\n" \
                "else:\n" \
                    "\t{target}.items['{id_}'] = [{new_item}, {quantity}]\n".format(target=target, id_=node.id_, original_count = original_count, quantity=node.quant, new_item=new_thing)
        else:
            attr = node.id_
            new_thing = node.id_.capitalize() + "()"
            return_stmt = "{target}.{attr} = {new_obj}".format(target=target, attr=attr, new_obj=new_thing)

        return return_stmt

    def generate_set(self, node):
        target = self.resolve_target(node.target)
        if node.val[0][0] == 'OBJ':
            value = self.resolve_target(node.val[0])
        else:
            value = node.val[1]

        return_stmt = "{target} = {value}\n".format(target=target, value=value)
        return return_stmt

    def generate_remove(self, node):
        target = self.resolve_target(node.from_)

        if self.get_type(node.id_) == 'ITEM':
            original_count = "{target}.items['{id_}'][1]".format(target=target, id_=node.id_)
            return_stmt = \
                "if '{id_}' in {target}.items:\n" \
                    "\t{target}.items['{id_}'][1] = {original_count} - {quantity}\n".format(target=target, id_=node.id_, original_count = original_count, quantity=node.quant)
        else:
            attr = node.id_
            return_stmt = "del {target}.{attr}".format(target=target, attr=attr)

        return return_stmt

    # generates code for move statement
    def generate_move(self, node):
        target = self.resolve_target(node.target)
        return "" + target + ".location = '" + node.new_loc[1].lower() + "'\n"

    # generates code for execute statement
    def generate_execute(self, node):
        function = self.resolve_target(node.func)
        args = []

        for arg in node.args:
            if type(arg[0]) == str and len(arg) == 1: #is a string literal
                args.append("'" + arg[0] + "'")
            elif arg[0] == 'LIT':
                args.append(arg[1])
            else:
                args.append(self.resolve_target(arg[0]))

        return_stmt = "{function}({args}, settings, player)".format(function=function, args=",".join(args))
        return return_stmt

    # creates code for increase
    def generate_increase(self, node):
        target = self.resolve_target(node.target)
        return_stmt = "" + target + "+=" + node.val[1]

        return return_stmt

    # creates code for decrease
    def generate_decrease(self, node):
        target = self.resolve_target(node.target)
        return_stmt = "" + target + "-=" + node.val[1]

        return return_stmt

    def generate_using(self, node):
        return "self.using='{filename}'".format(filename=node.filename)

    def generate_initiate(self, node):
        label = node.label.replace('#', '').replace(' ', '_').lower()
        return "Dialogue(self.using, settings, player, self).start_dialogue('{label}')".format(label=label)

    def generate_goto(self, node):
        label = node.label.replace('#', '').replace(' ', '_').lower()
        return_stmt = "self.goto('{label}')".format(label=label)
        return return_stmt

    def generate_exit(self, node):
        return "pass\n"

    def generate_label(self, node):
        label = node.label.replace('#', '').replace(' ', '_').lower()
        return_stmt = "def {label}(self):\n".format(label=label)
        for stmt in node.statements:
            s = self.generate_statement(stmt)
            for line in s.splitlines():
                return_stmt += '\t' + line + "\n"

        return return_stmt


    #Parses a TF or arithmetic expression
    def parse_expr(self, expr):
        ops = ['<', '>', '<=', '>=', '==', '!=', '+', '-', '*', '/', '%', '^']
        if len(expr) == 1: #String literal
            return "'" + expr + "'"
        if expr[0] in ['OBJ', 'LIT']:
            if expr[0] == 'OBJ':
                return self.resolve_target(expr)
            elif expr[0] == 'LIT':
                return expr[1]

        output = ""
        operands = []
        operator = expr[0]

        if len(expr) == 2: #unary op
            operands.append(expr[1][0])
        else:
            operands.append(expr[1])
            operands.append(expr[2])

        if operator == 'HAS':
            output += self.generate_has(expr)
        elif operator in ops:
            if len(operands) == 1:
                output += operator
                output += "(" +  self.parse_expr(operands[0]) + ")"
            else:
                output += "(" +  self.parse_expr(operands[0]) + ")"
                output += " " + operator + " "
                output += "(" + self.parse_expr(operands[1]) + ")"

        return output

    def generate_statement(self, node):
        stmt_map = {
            'ADD': self.generate_add,
            'PRINT': self.generate_print,
            'SET': self.generate_set,
            'REMOVE': self.generate_remove,
            'EXECUTE': self.generate_execute,
            'MOVE': self.generate_move,
            'INCREASE': self.generate_increase,
            'DECREASE': self.generate_decrease,
            'USING': self.generate_using,
            'INITIATE': self.generate_initiate,
            'GOTO': self.generate_goto,
            'EXIT': self.generate_exit,
        }

        if node.__class__.__name__ == 'Conditional':
            return self.generate_conditionals(node)
        else:
            return stmt_map[node.type_](node)

    def generate_conditionals(self, case_inst):
        cases = case_inst.cases
        output = ""

        for (counter, conditional) in enumerate(cases):
            if counter == 0:
                if_condition = cases[0][0]
                if_stmt_list = cases[0][1]
                output += "if {condition}:\n".format(condition=self.parse_expr(if_condition))

                for stmt in if_stmt_list:
                    s = self.generate_statement(stmt)
                    for line in s.splitlines():
                        output += "\t" + line + "\n"
            elif counter == len(cases) - 1 and True:
                else_stmt_list = cases[-1][1]
                output += 'else:\n'
                for stmt in else_stmt_list:
                    s = self.generate_statement(stmt)
                    for line in s.splitlines():
                        output += "\t" + line + "\n"
            else:
                elif_condition = cases[counter][0]
                elif_stmt_list = cases[counter][1]

                output += "elif {condition}:\n".format(condition=self.parse_expr(elif_condition))

                for stmt in elif_stmt_list:
                    s = self.generate_statement(stmt)
                    for line in s.splitlines():
                        output += "\t" + line + "\n"

        return output

    def generate_action(self, action_phrase, stmt_list):
        output = "def {action_phrase}(self, settings, player):\n".format(action_phrase=action_phrase)
        for stmt in stmt_list:
            s = self.generate_statement(stmt)
            for line in s.splitlines():
                output += "\t" + line + "\n"
        return output

    def generate_function(self, node):
        function_string = "def %s(self" % node.name
        for arg in node.arg_names:
            function_string += ", " + arg
        function_string += ", settings, player):\n"

        for stmt in node.statements:
            s =  self.generate_statement(stmt)
            for line in s.splitlines():
                function_string +=  '\t' + line + '\n'

        return function_string

    def generate_dialogue(self, node):
        output = ""
        f = open('generator/dialogue.py')
        theLabels = ""
        for line in f:
            output += line
            if line.strip() == "#1#": #Start generating labels here
                for lab in node:
                    lab = lab.label.replace('#', '').replace(' ', '_').lower()
                    theLabels = theLabels + "\t\tself.labels['{label}'] = self.{label}\n".format(label=lab)
                output += theLabels
            elif line.strip() == "#2#":
                for dialogue_node in node:
                    s = self.generate_label(dialogue_node)
                    for line in s.splitlines():
                        output += "\t" + line + "\n"

        output = output.replace("LAST_INPUT", "self.last_input")
        output = output.replace("player.", "self.player.")
        print output
        return output
            #replace with self.last_input
