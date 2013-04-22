import ply.lex as lex

def generate_lexer():

  reserved = {
      'ITEM' : 'ITEM',
      'CHARACTER' : 'CHARACTER',
      'TRAIT' : 'TRAIT',
      'SETTING' : 'SETTING',
      'START' : 'START',
      'ACTIONS' : 'ACTIONS',
      'FUNCTIONS' : 'FUNCTIONS',
      'DIALOGUE' : 'DIALOGUE',
      'INITIATE' : 'INITIATE',
      'AT' : 'AT',
      'GOTO' : 'GOTO',
      'LOCATION' : 'LOCATION',
      'ADD' : 'ADD',
      'SET' : 'SET',
      'ON' : 'ON',
      'HAS' : 'HAS',
      'REMOVE' : 'REMOVE',
      'FROM' : 'FROM',
      'EXECUTE' : 'EXECUTE',
      'WITH' : 'WITH',
      'MOVE' : 'MOVE',
      'TO' : 'TO',
      'INCREASE' : 'INCREASE',
      'BY' : 'BY',
      'DECREASE' : 'DECREASE',
      'IF' : 'IF',
      'ELSE' : 'ELSE',
      'PRINT' : 'PRINT',
      'INTEGER' : 'INTEGER',
      'DECIMAL' : 'DECIMAL',
      'TF' : 'TF',
      'STRING' : 'STRING',
      'TRUE' : 'TRUE',
      'FALSE' : 'FALSE',
      'USING' : 'USING',
      'EQUALS' : 'EQUALS',
      'NOT' : 'NOT',
      'OR' : 'OR',
      'AND' : 'AND',
#TODO: Player and Last_Input will be handled by the semantic analyzer
#      'PLAYER' : 'PLAYER',
#      'LAST_INPUT' : 'LAST_INPUT',
      'EXIT' : 'EXIT',
      'END_BLOCK' : 'END_BLOCK'
  }
  tokens = [
      'ID',
      'LABEL',
      'COLON',
      'COMMA',
      'INDENT',
      'CONCAT',
      'COMMENT',
      'INTEGER_VAL',
      'DECIMAL_VAL',
      'STRING_VAL',
      'LBRACE',
      'RBRACE',
      'ASSIGN',
      'PLUS',
      'MINUS',
      'MULTIPLY',
      'DIVIDE',
      'POWER',
      'LTHAN',
      'GTHAN',
      'LTHANEQ',
      'GTHANEQ',
      'ISEQUAL',
      'NOTEQUAL',
      'MODULUS',
      'LPAREN',
      'RPAREN'
  ] + list(reserved.values())
  
  def t_ID(t):
    r'[a-zA-Z][\w]*'
    t.type = reserved.get(t.value, 'ID')
    return t
  
  def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
  
  def t_error(t):
    import sys
    sys.stderr.write("Illegal character '%s'\n" % t.value[0])
    t.lexer.skip(1)

  t_ignore = ' '
  
  t_INDENT = r'\t'
  t_LABEL = r'\#[^\#]+\#'
  t_COLON = r':'
  t_COMMA = r','
  t_ignore_COMMENT = r'//.*'
  t_CONCAT = r'\.'
  t_INTEGER_VAL = r'([1-9]\d*|0)'
  t_DECIMAL_VAL = r'\d+\.\d+'
  t_STRING_VAL = r'"([^\\"]|\\")*"'
  t_LBRACE = r'{'
  t_RBRACE = r'}'
  t_ASSIGN = r'='
  t_PLUS = r'\+'
  t_MINUS = r'-'
  t_MULTIPLY = r'\*'
  t_DIVIDE = r'/'
  t_POWER = r'\^'
  t_LTHAN = r'<'
  t_GTHAN = r'>'
  t_LTHANEQ = r'<='
  t_GTHANEQ = r'>='
  t_ISEQUAL = r'=='
  t_NOTEQUAL = r'!='
  t_MODULUS = r'%'
  t_LPAREN = r'\('
  t_RPAREN = r'\)'
  
  lexer = lex.lex()
  return (lexer, tokens)

