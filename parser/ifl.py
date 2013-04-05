import ply.lex as lex

def generate_lexer():

  reserved = {
      'PLAYER' : 'PLAYER',
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
      'EXIT' : 'EXIT',
      'LOCATION' : 'LOCATION',
      'LAST_INPUT' : 'LAST_INPUT',
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
      'FALSE' : 'FALSE'
  }
  tokens = [
      'ID',
      'LABEL',
      'COLON',
      'INDENT',
      'CONCAT',
      'INTEGER_VAL',
      'DECIMAL_VAL',
      'STRING_VAL',
      'LBRACE',
      'RBRACE',
      'EQUALS',
      'PLUS',
      'MINUS',
      'MULTIPLY',
      'DIVIDE',
      'POWER',
      'LTHAN',
      'GTHAN',
      'LTHANEQ',
      'GTHANEQ',
      'MODULUS',
      'LPAREN',
      'RPAREN'
  ] + list(reserved.values())
  
  def t_ID(t):
    r'[a-zA-Z][\w]+'
    t.type = reserved.get(t.value, 'ID')
    return t
  
  def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)
  t_ignore = ' '
  
  t_INDENT = r'\t'
  t_LABEL = r'\#[\w ]+'
  t_COLON = r':'
  t_CONCAT = r'\.'
  t_INTEGER_VAL = r'([1-9]\d*|0)'
  t_DECIMAL_VAL = r'\d+\.\d+'
  t_STRING_VAL = r'"([^\\"]|\\")*"'
  t_LBRACE = r'{'
  t_RBRACE = r'}'
  t_EQUALS = r'='
  t_PLUS = r'\+'
  t_MINUS = r'-'
  t_MULTIPLY = r'\*'
  t_DIVIDE = r'/'
  t_POWER = r'\^'
  t_LTHAN = r'<'
  t_GTHAN = r'>'
  t_LTHANEQ = r'<='
  t_GTHANEQ = r'>='
  t_MODULUS = r'%'
  t_LPAREN = r'\('
  t_RPAREN = r'\)'
  
  lexer = lex.lex()
  return lexer

