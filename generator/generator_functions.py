from analyzer.nodes1 import Conditional

# generates a print statement
#'print : PRINT string_expression'
#node is the statement node
#id is the id of the top level in which the statement is defined in
#tree is the semantic tree


class FunctionGenerator():
    def __init__(self, id_, tree):
        self.id_ = id_
        self.tree = tree

    def get_type(self, id_):
        try:
            return self.tree.def_types[id_]
        except KeyError:
            return None

    def resolve_target(self, target_list):
        if target_list[0] == 'OBJ':
            target_list = target_list[1:]
        if target_list[0] == self.id_:
            target_list[0] = 'self'
        target_string = '.'.join(target_list)
        return target_string

    def generate_has(self, node):
        holdee = node[2]
        holder = self.resolve_target(node[1])

        if self.get_type(holdee) == 'ITEM':
            a = "'{holdee}' in {holder}.items and {holder}.items['{holdee}'][1] > 0".format(holder=holder, holdee=holdee)
            print a
        else:
            return "hasattr({holder}, {holdee})".format(holder=holder, holdee=holdee)

    def generate_print(self, node):
        return "print \"" + node.string_expr[0] + "\"\n"

    #TODO test if add and set work for strings and decimals, differentiate between strings and ints
    def generate_add(self, node):
        target = self.resolve_target(node.to)

        if node.primitive:
            attr = node.primitive.name
            val = node.primitive.val[1]
            return_stmt = "{target}.{attr} = {value}".format(target=target, attr=attr, value=val)
        elif self.get_type(node.id_) == 'ITEM':
            original_count = "{target}.items[{id_}][1]".format(target=target, id_=node.id_)
            new_thing = node.id_.capitalize() + "()"
            return_stmt =\
                "if {id_} in {target}.items:\n" \
                    "\t{target}.items['{id_}'][1] = {original_count} + {quantity}\n" \
                "else:\n" \
                    "\t{target}.items['{id_}'] = ({new_item}, {quantity})\n".format(target=target, id_=node.id_, original_count = original_count, quantity=node.quant, new_item=new_thing)
        else:
            attr = node.id_
            new_thing = node.id_.capitalize() + "()"
            return_stmt = "{target}.{attr} = {new_obj}".format(target=target, attr=attr, new_obj=new_thing)

        return return_stmt

    def generate_set(self, node):
        target = self.resolve_target(node.target)
        value = node.val[1]
        return_stmt = "{target} = {value}".format(target=target, value=value)

        return return_stmt

    def generate_remove(self, node):
        return "pass\n"

    # moves player
    def generate_move(self, node):
        return "pass\n"

    def generate_execute(self, node):
        return "pass\n"

    def generate_increase(self, node):
        return "pass\n"

    def generate_decrease(self, node):
        return "pass\n"

    def parse_tf_expr(self, expr):
        if expr[0] == 'HAS':
            return self.generate_has(expr)
        else:
            #TODO parse other TF expressions here
            pass

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
                output += "if {condition}:\n".format(condition=self.parse_tf_expr(if_condition))

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

        #test nested statements
        return output

    def generate_action(self, action_phrase, stmt_list):
        output = "def {action_phrase}():".format(action_phrase=action_phrase)
        for stmt in stmt_list:
            s = self.generate_statement(stmt)
            for line in s.splitlines():
                output += "\t" + line + "\n"
        return output

    def generate_function(self, node):
        function_string = "def %s(self" % node.name
        for arg in node.arg_names:
            function_string += ", " + arg
        function_string += "):\n"

        for stmt in node.statements:
            s =  self.generate_statement(stmt)
            for line in s.splitlines():
                function_string +=  '\t' + line + '\n'

        return function_string
