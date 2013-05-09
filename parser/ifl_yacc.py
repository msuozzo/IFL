import ply.yacc as yacc

def generate_parser(lexer, tokens):
  start = 'program'

  precedence = (
      ('nonassoc', 'LTHAN', 'GTHAN', 'LTHANEQ', 'GTHANEQ', 'ISEQUAL', 'NOTEQUAL'),
      ('left', 'OR', 'AND', 'PLUS', 'MINUS', 'MODULUS'),
      ('left', 'DIVIDE', 'MULTIPLY'),
      ('right', 'NOT', 'UMINUS'),
      ('left', 'CONCAT', 'ON'),
  )
  def p_empty(p):
    'empty :'
    pass

  def p_program(p):
    '''program : program definition
               | empty'''
    p[0] = () if len(p) == 2 else (p[2],) + p[1]

  def p_definition(p):
    '''definition : trait_definition
                  | character_definition
                  | setting_definition
                  | item_definition'''
    p[0] = p[1]

  def p_trait_definition(p):
    'trait_definition : TRAIT ID COLON desc_or_nothing s_directive f_or_nothing END_BLOCK'
    p[0] = (p[1], p[2], p[4], p[5], p[6])

  def p_character_definition(p):
    'character_definition : CHARACTER ID COLON desc_or_nothing s_directive a_or_nothing f_or_nothing d_or_nothing END_BLOCK'
    p[0] = (p[1], p[2], p[4], p[5], p[6], p[7], p[8])

  def p_setting_definition(p):
    'setting_definition : SETTING ID COLON desc_or_nothing s_directive END_BLOCK'
    p[0] = (p[1], p[2], p[4], p[5])

  def p_item_definition(p):
    'item_definition : ITEM ID COLON desc_or_nothing s_directive a_or_nothing f_or_nothing END_BLOCK'
    p[0] = (p[1], p[2], p[4], p[5], p[6], p[7])

  def p_desc_or_nothing(p):
    '''desc_or_nothing : description_string
                       | empty'''
    p[0] = p[1]

  def p_description_string(p):
    'description_string : string_value'
    p[0] = p[1]

#  def p_id_or_player(p):
#    '''id_or_player : ID
#                    | PLAYER'''
#    p[0] = p[1]

  def p_s_directive(p):
    's_directive : START COLON start_list END_BLOCK'
    p[0] = (p[1], p[3])

  def p_start_list(p):
    'start_list : statement_list'
    p[0] = p[1]

  def p_d_or_nothing(p):
    '''d_or_nothing : d_directive
                    | empty'''
    p[0] = p[1]

  def p_d_directive(p):
    'd_directive : DIALOGUE COLON dialogue_list END_BLOCK'
    p[0] = (p[1], p[3])

  def p_dialogue_list(p):
    '''dialogue_list : LABEL COLON statement_list END_BLOCK dialogue_list
                     | empty'''
    if len(p) != 2: p[0] = ((p[1], p[3]),) + p[5]
    else: p[0] = ()

  def p_a_or_nothing(p):
    '''a_or_nothing : a_directive
                    | empty'''
    p[0] = p[1]

  def p_a_directive(p):
    'a_directive : ACTIONS COLON action_list END_BLOCK'
    p[0] = (p[1], p[3])

  def p_action_list(p):
    '''action_list : string_value COLON statement_list END_BLOCK action_list
                   | empty'''
    if len(p) != 2: p[0] = ((p[1], p[3]),) + p[5]
    else: p[0] = ()

  def p_f_or_nothing(p):
    '''f_or_nothing : f_directive
                    | empty'''
    p[0] = p[1]

  def p_f_directive(p):
    'f_directive : FUNCTIONS COLON function_list END_BLOCK'
    p[0] = (p[1], p[3])

  def p_function_list(p):
    '''function_list : function_list ID args_or_nothing COLON statement_list END_BLOCK
                     | empty'''
    if len(p) != 2: p[0] = ((p[2], p[3], p[5]),) + p[1]
    else: p[0] = ()

  def p_args_or_nothing(p):
    '''args_or_nothing : WITH ID optional_args
                       | empty'''
    p[0] = None if len(p) == 2 else (p[2],) + p[3]

  def p_optional_args(p):
    '''optional_args : optional_args COMMA ID
                     | empty'''
    p[0] = () if len(p) == 2 else (p[3],) + p[1]

  def p_statement_list(p):
    '''statement_list : statement_list statement
                      | empty'''
    p[0] = () if len(p) == 2 else p[1] + (p[2],)

  def p_statement(p):
    '''statement : print
                 | add
                 | remove
                 | set
                 | move
                 | increase
                 | decrease
                 | initiate
                 | conditional
                 | execute
                 | goto
                 | using
                 | EXIT'''
    p[0] = p[1]

  def p_conditional(p):
    '''conditional : IF tf_expression COLON statement_list END_BLOCK else_if_conditional else_conditional'''
    p[0] = (p[1], (p[2], p[4])) + p[6] + (p[7],)

  def p_else_if_conditional(p):
    '''else_if_conditional : else_if_conditional ELSE IF tf_expression COLON statement_list END_BLOCK
                           | empty'''
    p[0] = () if len(p) == 2 else ((p[4], p[6]),) + p[1]

  def p_else_conditional(p):
    '''else_conditional : ELSE COLON statement_list END_BLOCK
                        | empty'''
    p[0] = None if len(p) == 2 else (None, p[3])

  def p_goto(p):
    'goto : GOTO LABEL'
    p[0] = (p[1], p[2])

  def p_execute(p):
    'execute : EXECUTE object_chain passed_args'
    p[0] = (p[1], p[2], p[3])

  def p_passed_args(p):
    '''passed_args : WITH arg optional_passed_args
                   | empty'''
    p[0] = None if len(p) == 2 else (p[2],) + p[3]

  def p_optional_passed_args(p):
    '''optional_passed_args : optional_passed_args COMMA arg
                            | empty'''
    p[0] = () if len(p) == 2 else (p[3],) + p[1]

  def p_arg(p):
    '''arg : arithmetic_expression
           | string_expression
           | tf_expression'''
    p[0] = p[1]

  def p_print(p):
    'print : PRINT string_expression'
    p[0] = (p[1], p[2])

  def p_add(p):
    '''add : ADD quantity ID TO object_chain
           | ADD primitive TO object_chain'''
    if len(p) == 6: p[0] = (p[1], p[2], p[3], p[5])
    else: p[0] = (p[1], None, p[2], p[4])

  def p_quantity(p):
    '''quantity : LBRACK arithmetic_expression RBRACK
                | empty'''
    p[0] = p[1]

  def p_arithmetic_expression(p):
    '''arithmetic_expression : arithmetic_or_object PLUS arithmetic_or_object
                             | arithmetic_or_object MINUS arithmetic_or_object
                             | arithmetic_or_object MODULUS arithmetic_or_object
                             | arithmetic_or_object DIVIDE arithmetic_or_object
                             | arithmetic_or_object MULTIPLY arithmetic_or_object
                             | arithmetic_or_object POWER arithmetic_or_object
                             | MINUS arithmetic_or_object %prec UMINUS
                             | LPAREN arithmetic_or_object RPAREN
                             | INTEGER_VAL
                             | DECIMAL_VAL'''
    if len(p) == 4:
      if p[1] == '(': p[0] = p[2]
      else: p[0] = (p[2], p[1], p[3])
    elif len(p) == 3:
      p[0] = (p[1], p[2])
    else: p[0] = p[1]

  def p_to_or_nothing(p):
    '''to_or_nothing : TO object_chain
                     | empty'''
    if len(p) == 3: p[0] = p[2]
    elif len(p) == 2: p[0] = None

  def p_object_chain(p):
    '''object_chain : object_chain ON ID
                    | ID'''
    if len(p) == 4: p[0] = (p[3],) + p[1]
    elif len(p) == 2: p[0] = (p[1],)

  def p_primitive(p):
    '''primitive : integer_primitive
                 | decimal_primitive
                 | string_primitive
                 | tf_primitive'''
    p[0] = p[1]

  def p_integer_primitive(p):
    'integer_primitive : LBRACE INTEGER ID ASSIGN numeric_literal RBRACE'
    p[0] = (p[2], p[3], p[5])

  def p_decimal_primitive(p):
    'decimal_primitive : LBRACE DECIMAL ID ASSIGN numeric_literal RBRACE'
    p[0] = (p[2], p[3], p[5])

  def p_string_primitive(p):
    'string_primitive : LBRACE STRING ID ASSIGN string_expression RBRACE'
    p[0] = (p[2], p[3], p[5])

  def p_tf_primitive(p):
    'tf_primitive : LBRACE TF ID ASSIGN tf_expression RBRACE'
    p[0] = (p[2], p[3], p[5])

  def p_numeric_literal(p):
    '''numeric_literal : arithmetic_expression
                       | object_chain'''
    p[0] = p[1]

  def p_string_value(p):
    '''string_value : STRING_VAL'''
    p[0] = p[1].strip('"')

  def p_string_expression(p):
    '''string_expression : string_expression CONCAT string_literal
                         | string_literal'''
    if len(p) == 4: p[0] = (p[3],) + p[1]
    else: p[0] = (p[1],)

  def p_string_literal(p):
    '''string_literal : string_value
                      | object_chain'''
    p[0] = p[1]

  def p_tf_expression(p):
    '''tf_expression : tf_expression OR tf_expression
                     | tf_expression AND tf_expression
                     | NOT tf_expression
                     | LPAREN tf_expression RPAREN
                     | tf_literal'''
    if len(p) == 4:
      if p[1] == '(': p[0] = p[2]
      else: p[0] = (p[1], p[2]) + p[3]
    elif len(p) == 3: p[0] = (p[1], p[2])
    elif len(p) == 2: p[0] = p[1]

  def p_tf_literal(p):
    '''tf_literal : has_expression
                  | relational_expression
                  | TRUE
                  | FALSE'''
    p[0] = p[1]

  def p_relational_operand(p):
    '''relational_operand : tf_literal
                          | object_chain
                          | arithmetic_expression
                          | string_value'''
    p[0] = p[1]

  def p_has_expression(p):
    '''has_expression : object_chain HAS ID
                      | HAS ID'''
    if len(p) == 4: p[0] = (p[2], p[1], p[3])
    else: p[0] = (p[1], None, p[2])

  def p_relational_expression(p):
    'relational_expression : relational_operand relational_operator relational_operand'
    p[0] = (p[2], p[1], p[3])

  def p_relational_operator(p):
    '''relational_operator : LTHAN
                           | GTHAN
                           | LTHANEQ
                           | GTHANEQ
                           | ISEQUAL
                           | NOTEQUAL
                           | EQUALS
                           | NOT EQUALS''' 
    if len(p) == 2:
      if p[1] == 'EQUALS': p[0] = '=='
      else: p[0] = p[1]
    else: p[0] = '!='

  def p_remove(p):
    '''remove : REMOVE quantity ID from_or_nothing'''
    p[0] = (p[1], p[2], p[3], p[4])

  def p_from_or_nothing(p):
    '''from_or_nothing : FROM object_chain
                       | empty'''
    if len(p) == 3: p[0] = p[2]
    elif len(p) == 2: p[0] = None

  def p_set(p):
    '''set : SET object_chain TO arg'''
    p[0] = (p[1], p[2], p[4])

  def p_move(p):
    'move : MOVE character_or_nothing TO object_chain'
    p[0] = (p[1], p[2], p[4])

  def p_character_or_nothing(p):
    '''character_or_nothing : object_chain
                            | empty'''
    p[0] = p[1]

  def p_arithmetic_or_object(p):
      '''arithmetic_or_object : arithmetic_expression
                            | object_chain'''
      p[0] = p[1]

  def p_increase(p):
    'increase : INCREASE object_chain BY arithmetic_or_object'
    p[0] = (p[1], p[2], p[4])

  def p_decrease(p):
    'decrease : DECREASE object_chain BY arithmetic_or_object'
    p[0] = (p[1], p[2], p[4])

  def p_initiate(p):
    'initiate : INITIATE DIALOGUE AT LABEL'
    p[0] = (p[1], p[4])

  def p_using(p):
    'using : USING string_value'
    p[0] = (p[1], p[2])


  def p_error(p):
    print p
    print "Syntax error in input!"

  return yacc.yacc()


