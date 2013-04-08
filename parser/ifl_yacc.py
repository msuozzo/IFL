import ply.yacc as yacc

def generate_parser(lexer, tokens):
  start = 'program'

  precedence = (
      ('left', 'OR', 'AND'),
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
    'definition : trait_definition'
    p[0] = p[1]

  def p_trait_definition(p):
    'trait_definition : TRAIT trait_identifier COLON desc_or_nothing s_directive'
#    'trait_definition : TRAIT trait_identifier INDENT description_string INDENT s_directive INDENT f_directive'
    #TODO: Implement f_directive
    p[0] = (p[2], p[4], p[5])

  def p_desc_or_nothing(p):
    '''desc_or_nothing : INDENT description_string
                       | empty'''
    p[0] = p[1] if len(p) == 2 else p[2]

  def p_trait_identifier(p):
    'trait_identifier : ID'
    p[0] = p[1]

  def p_description_string(p):
    'description_string : STRING_VAL'
    p[0] = p[1]

  def p_s_directive(p):
    's_directive : INDENT START COLON start_list'
    p[0] = p[5]

  def p_start_list(p):
    'start_list : statement_list'
    p[0] = p[1]

  def p_statement_list(p):
    '''statement_list : INDENT INDENT statement statement_list
                      | empty'''
    p[0] = p[4] + [p[3]] if p[1] else []

  def p_statement(p):
    '''statement : print
                 | add
                 | remove
                 | move
                 | increase
                 | decrease
                 | initiate
                 | conditional
                 | using'''
#    '''statement : execute
#                 | print
    p[0] = p[1]


  def p_conditional(p):
    '''conditional : IF tf_expression'''
    pass

#TODO: implement functions
#  def p_execute(p):
#    'execute : EXECUTE function_id optional_args'
#    p[0] = tuple(p[1:])
#
#  def p_function_id(p):
#    'function_id : ID'
#    p[0] = p[1]
#
#  def p_optional_args(p):
#    ''
#    p[0] = p[1]

  def p_print(p):
    'print : PRINT string_expression'
    p[0] = tuple(p[1:])

  def p_add(p):
    '''add : ADD quantity object_identifier to_or_nothing
           | ADD primitive to_or_nothing'''
    p[0] = tuple(p[1:])

  def p_quantity(p):
    '''quantity : arithmetic_expression
                | empty'''
    p[0] = p[1]

  def p_arithmetic_expression(p):
    'arithmetic_expression : INTEGER_VAL'
    #TODO: Finish arithmetic expressions
    p[0] = p[1]

  def p_object_identifier(p):
    'object_identifier : ID'
    p[0] = p[1]

  def p_to_or_nothing(p):
    '''to_or_nothing : TO object_chain
                     | empty'''
    if len(p) == 3:
      p[0] = p[2]
    elif len(p) == 2:
      p[0] = None

  def p_object_chain(p):
    '''object_chain : object_identifier ON object_chain
                    | object_identifier'''
    if len(p) == 4:
      p[0] = [p[1]] + p[3]
    elif len(p) == 2:
      p[0] = [p[1]]

  def p_primitive(p):
    '''primitive : integer_primitive
                 | decimal_primitive
                 | string_primitive
                 | tf_primitive'''
    p[0] = p[1]

  def p_integer_primitive(p):
    'integer_primitive : LBRACE INTEGER ID ASSIGN arithmetic_expression RBRACE'
    p[0] = (p[2], p[3], p[5])

  def p_decimal_primitive(p):
    'decimal_primitive : LBRACE DECIMAL ID ASSIGN arithmetic_expression RBRACE'
    p[0] = (p[2], p[3], p[5])

  def p_string_primitive(p):
    'string_primitive : LBRACE STRING ID ASSIGN string_expression RBRACE'
    p[0] = (p[2], p[3], p[5])

  def p_tf_primitive(p):
    'tf_primitive : LBRACE TF ID ASSIGN tf_expression RBRACE'
    p[0] = (p[2], p[3], p[5])

  def p_string_expression(p):
    '''string_expression : string_literal CONCAT string_expression
                         | string_literal'''
    if len(p) == 4:
      p[0] = [p[1]] + p[3]
    else:
      p[0] = [p[1]]

  def p_string_literal(p):
    '''string_literal : STRING_VAL
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
      else: p[0] = [p[1], p[2]] + p[3]
    elif len(p) == 3: p[0] = [p[1], p[2]]
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
    if len(p) == 4:
      p[0] = (p[2], p[1], p[3])
    else:
      p[0] = (p[1], None, p[2])

  def p_relational_expression(p):
    'relational_expression : arithmetic_expression relational_operator arithmetic_expression'
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
    p[0] = tuple(p[1:])

  def p_from_or_nothing(p):
    '''from_or_nothing : FROM object_chain
                       | empty'''
    if len(p) == 3:
      p[0] = p[2]
    elif len(p) == 2:
      p[0] = None

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
    'using : USING STRING_VAL'
    p[0] = (p[1], p[2])



  def p_error(p):
    print p
    print "Syntax error in input!"

  return yacc.yacc()


