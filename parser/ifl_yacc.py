import ply.yacc as yacc

def generate_parser(lexer, tokens):
  start = 'program'

  precedence = (
      ('left', 'OR', 'AND', 'PLUS', 'MINUS'),
      ('left', 'DIVIDE', 'MULTIPLY'),
      ('right', 'NOT')
  )
  def p_empty(p):
    'empty :'
    pass

  def p_program(p):
    '''program : definition program
               | empty'''
    p[0] = p[1]
    if p[0]:
      for sec in p[0]: print sec

  def p_definition(p):
    '''definition : trait_definition
                  | character_definition
                  | setting_definition
                  | item_definition'''
    p[0] = p[1]

  def p_trait_definition(p):
    'trait_definition : TRAIT ID COLON desc_or_nothing s_directive f_directive END_BLOCK'
    p[0] = (p[1], p[2], p[4], p[5], p[6])

  def p_character_definition(p):
    'character_definition : CHARACTER id_or_player COLON desc_or_nothing s_directive a_or_nothing f_or_nothing d_or_nothing END_BLOCK'
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

  def p_id_or_player(p):
    '''id_or_player : ID
                    | PLAYER'''
    p[0] = p[1]

  def p_s_directive(p):
    's_directive : START COLON start_list END_BLOCK'
    p[0] = (p[1], p[3])

  def p_start_list(p):
    'start_list : statement_list'
    p[0] = tuple(p[1])

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
    '''function_list : ID args_or_nothing COLON statement_list function_list END_BLOCK
                     | empty'''
    if len(p) != 2: p[0] = ((p[1], p[2], p[4]),) + p[5]
    else: p[0] = ()

  def p_args_or_nothing(p):
    '''args_or_nothing : WITH ID optional_args
                       | empty'''
    p[0] = None if len(p) == 2 else (p[2],) + p[3]

  def p_optional_args(p):
    '''optional_args : COMMA ID optional_args
                     | empty'''
    p[0] = () if len(p) == 2 else (p[2],) + p[3]

  def p_statement_list(p):
    '''statement_list : statement statement_list
                      | empty'''
    p[0] = () if not p[1] else p[2] + (p[1],)

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
                 | using'''
    p[0] = p[1]

  def p_conditional(p):
    '''conditional : IF tf_expression COLON statement_list END_BLOCK else_if_conditional else_conditional'''
    p[0] = (p[1], (p[2], p[4])) + p[6] + (p[7],)

  def p_else_if_conditional(p):
    '''else_if_conditional : ELSE IF tf_expression COLON statement_list END_BLOCK else_if_conditional
                           | empty'''
    if len(p) != 2: p[0] = ((p[3], p[5]),) + p[7]
    else: p[0] = ()

  def p_else_conditional(p):
    '''else_conditional : ELSE COLON statement_list END_BLOCK
                        | empty'''
    if len(p) != 2: p[0] = (None, p[3])
    else: p[0] = None

  def p_goto(p):
    'goto : GOTO LABEL'
    p[0] = (p[1], p[2])

  def p_execute(p):
    'execute : EXECUTE ID passed_args'
    p[0] = (p[1], p[2], p[3])

  def p_passed_args(p):
    '''passed_args : WITH arg optional_passed_args
                   | empty'''
    if len(p) != 2: p[0] = (p[2],) + p[3]
    else: p[0] = None

  def p_optional_passed_args(p):
    '''optional_passed_args : COMMA arg optional_passed_args
                            | empty'''
    p[0] = () if len(p) == 2 else (p[2],) + p[3]

  def p_arg(p):
    '''arg : object_chain
           | arithmetic_expression
           | string_expression
           | tf_expression'''
    p[0] = p[1]

  def p_print(p):
    'print : PRINT string_expression'
    p[0] = (p[1], p[2])

  def p_add(p):
    '''add : ADD quantity object_identifier to_or_nothing
           | ADD primitive to_or_nothing'''
    if len(p) == 5: p[0] = (p[1], p[3], p[4], p[2])
    else: p[0] = (p[1], p[2], p[3], None)

  def p_quantity(p):
    '''quantity : arithmetic_expression
                | empty'''
    p[0] = p[1]

  def p_arithmetic_expression(p):
    '''arithmetic_expression : INTEGER_VAL
                             | DECIMAL_VAL'''
    #TODO: Finish arithmetic expressions
    p[0] = p[1]

  def p_object_identifier(p):
    'object_identifier : ID'
    p[0] = p[1]

  def p_to_or_nothing(p):
    '''to_or_nothing : TO object_chain
                     | empty'''
    if len(p) == 3: p[0] = p[2]
    elif len(p) == 2: p[0] = None

  def p_object_chain(p):
    '''object_chain : object_identifier ON object_chain
                    | object_identifier'''
    if len(p) == 4: p[0] = (p[1],) + p[3]
    elif len(p) == 2: p[0] = (p[1],)

  def p_primitive(p):
    '''primitive : integer_primitive
                 | decimal_primitive
                 | string_primitive
                 | tf_primitive
                 | ID'''
    p[0] = p[1]

  def p_integer_primitive(p):
    'integer_primitive : LBRACE INTEGER ID ASSIGN integral_literal RBRACE'
    p[0] = (p[2], p[3], p[5])

  def p_decimal_primitive(p):
    'decimal_primitive : LBRACE DECIMAL ID ASSIGN decimal_literal RBRACE'
    p[0] = (p[2], p[3], p[5])

  def p_string_primitive(p):
    'string_primitive : LBRACE STRING ID ASSIGN string_expression RBRACE'
    p[0] = (p[2], p[3], p[5])

  def p_tf_primitive(p):
    'tf_primitive : LBRACE TF ID ASSIGN tf_expression RBRACE'
    p[0] = (p[2], p[3], p[5])

  def p_integral_literal(p):
    '''integral_literal : INTEGER_VAL
                        | arithmetic_expression
                        | object_chain'''
    p[0] = p[1]

  def p_decimal_literal(p):
    '''decimal_literal : DECIMAL_VAL
                       | arithmetic_expression
                       | object_chain'''
    p[0] = p[1]

  def p_string_value(p):
    '''string_value : STRING_VAL'''
    p[0] = p[1].strip('"')

  def p_string_expression(p):
    '''string_expression : string_literal CONCAT string_expression
                         | string_literal'''
    if len(p) == 4: p[0] = (p[1],) + p[3]
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
    '''tf_literal : object_chain
                  | has_expression
                  | relational_expression
                  | TRUE
                  | FALSE'''
    p[0] = p[1]

  def p_has_expression(p):
    '''has_expression : ID HAS ID
                      | HAS ID'''
    if len(p) == 4: p[0] = (p[2], p[1], p[3])
    else: p[0] = (p[1], None, p[2])

  def p_relational_expression(p):
    'relational_expression : arg relational_operator arg'
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
    if len(p) == 2: p[0] = p[1]
    else: p[0] = '!='

  def p_remove(p):
    '''remove : REMOVE quantity object_identifier from_or_nothing
              | REMOVE primitive from_or_nothing'''
    if len(p) == 5: p[0] = (p[1], p[3], p[4], p[2])
    else: p[0] = (p[1], p[2], p[3], None)

  def p_from_or_nothing(p):
    '''from_or_nothing : FROM object_chain
                       | empty'''
    if len(p) == 3: p[0] = p[2]
    elif len(p) == 2: p[0] = None

  def p_set(p):
    '''set : SET object_chain TO primitive'''
    p[0] = (p[1], p[2], p[4])

  def p_move(p):
    'move : MOVE character_or_nothing TO object_chain'
    p[0] = p[2]

  def p_character_or_nothing(p):
    '''character_or_nothing : character_identifier
                            | empty'''
    p[0] = p[1]

  def p_character_identifier(p):
    'character_identifier : ID'
    p[0] = p[1]

  def p_increase(p):
    'increase : INCREASE object_chain BY arithmetic_expression'
    p[0] = (p[1], p[2], p[4])

  def p_decrease(p):
    'decrease : DECREASE object_chain BY arithmetic_expression'
    p[0] = (p[1], p[2], p[4])

  def p_initiate(p):
    'initiate : INITIATE DIALOGUE AT label_identifier'
    p[0] = (p[1], p[4])

  def p_label_identifier(p):
    'label_identifier : LABEL'
    p[0] = p[1]

  def p_using(p):
    'using : USING string_value'
    p[0] = (p[1], p[2])



  def p_error(p):
    print p
    print "Syntax error in input!"

  return yacc.yacc()


