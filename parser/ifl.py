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
      'EXIT' : 'EXIT',
      'LOCATION' : 'LOCATION',
      'LAST_INPUT' : 'LAST_INPUT',
      'ADD' : 'ADD',
      'SET' : 'SET',
      'TO' : 'TO',
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
      'STRING' : 'STRING'
  }
  tokens = [
      'ID',
      'LABEL',
      'COLON',
      'INDENT',
      'INTEGER_VAL',
      'DECIMAL_VAL',
      'TF_VAL',
      'STRING_VAL'
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
  
  lexer = lex.lex()
  return lexer

