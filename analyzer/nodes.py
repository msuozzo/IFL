

class Program:
  def __init__(self):
    self.definitions


class TLT:
  TRAIT = "TRAIT"
  ITEM = "ITEM"
  CHARACTER = "CHARACTER"
  SETTING = "SETTING"

  def __init__(self, type_, id_, desc, start, action, function, dialogue):
    self.type_ = type_
    self.id_ = id_
    self.desc = desc if desc is None else gen_desc(type_, id_)
    self.start = [stat_or_cond(tup, self.id_) for tup in start]
    self.actions = [Action(tup, self.id_) for tup in action[1]]
    self.functions = [Function(tup, self.id_) for tup in function[1]]
    self.dialogue = Dialogue(dialogue, self.id_)

  def gen_possible_fields(self):
    names = []
    for statement in self.start:
      names.extend(statement.get_add_fields())

  def get_add_fields(self):
    ret = []
    for stat in self.start: ret.extend(stat.get_add_fields())
    for action in self.actions: ret.extend(action.get_add_fields())
    for function in self.functions: ret.extend(function.get_add_fields())
    ret.extend(self.dialogue.get_add_fields())
    return ret


class Statement:
  ADD="ADD"
  PRINT="PRINT"
  REMOVE="REMOVE"
  SET="SET"
  MOVE="MOVE"
  INCREASE="INCREASE"
  DECREASE="DECREASE"
  INITIATE="INITIATE"
  EXECUTE="EXECUTE"
  GOTO="GOTO"
  USING="USING"

  def __init__(self, tup, tlt_name):
    self.type_ = tup[0]
    if self.type_ == Statement.ADD:
      self.id_ = tup[2]
      self.quant = tup[1] if tup[1] else 1
      self.to = tup[3] if tup[3] else (tlt_name,)
    elif self.type_ == Statement.PRINT:
      self.string_expr = tup[1]
    elif self.type_ == Statement.REMOVE:
      self.id_ = tup[2]
      self.quant = tup[1] if tup[1] else 1
      self.from_ = tup[3] if tup[3] else (tlt_name,)
    elif self.type_ == Statement.SET:
      self.target = tup[1]
      self.val = tup[2]
    elif self.type_ == Statement.MOVE:
      self.target = tup[1]
      self.new_loc = tup[2]
    elif self.type_ == Statement.INCREASE:
      self.target = tup[1]
      self.val = tup[2]
    elif self.type_ == Statement.DECREASE:
      self.target = tup[1]
      self.val = tup[2]
    elif self.type_ == Statement.INITIATE:
      self.label = tup[1]
    elif self.type_ == Statement.EXECUTE:
      self.func = tup[1]
      self.args = tup[2]
    elif self.type_ == Statement.GOTO:
      self.label = tup[1]
    elif self.type_ == Statement.USING:
      self.filename = tup[1]

  #FIX: "PLAYER ON House" may be stupid but it fails
  def get_add_fields(self):
    return [(self.to[0], self.id_)] if self.type_ == Statement.ADD else []


class Conditional(Statement):
  def __init__(self, tup, tlt_name):
    # contains 2-tuple of (case, statement_list)
    self.cases = []
    for sec in tup[1:]:
      if not sec: continue  #should activate on abscent ELSE clause
      case = sec[0]
      statements = [stat_or_cond(stat, tlt_name) for stat in sec[1:]]
      self.cases.append((case, statements))
    self.get_add_fields = lambda: get_add_fields(self.cases)


class Function:
  def __init__(self, tup, tlt_name):
    self.arguments = 
    self.statements
    self.get_add_fields = lambda: get_add_fields(self.statements)
 

class Action:
  def __init__(self, tup, tlt_name):
    self.action_phrase = tup[0]
    self.statements = []
    self.get_add_fields = lambda: get_add_fields(self.statements)
    pass

class Primitive:
  def __init__(self, tup, tlt_name):
    pass



def get_add_fields(lst):
  ret = []
  for elem in lst: ret.extend(elem.get_add_fields())
  return ret

def stat_or_cond(tup, tlt_name):
  return Conditional(tup, tlt_name) if tup[0] == "IF" else Statement(tup, tlt_name)

class Node:
	def __init__(self, data):
		self.data = data
		self.children = []

	def add_child(self, obj):
		self.children.append(obj)

	def add_child_front(self, obj):
		self.children.insert(0, obj)

	def get_children(self):
		return self.children

class DefinitionNode(Node):
	""" Possible DefinitionNodes include:
		trait_definitions
		character_definitions
		setting_definitions
		item_definitions

		DefinitionNodes must contain a type
		TRAIT/CHARACTER/SETTING/ITEM along with an ID
	"""
	def __init__(self, type_, ID):
		self.type_ = type_
		self.ID = ID
		self.parameters = []
		# self.description = []
		# self.start = []
		# self.functions = []
		# self.actions = []
		# self.dialogues = []
		print "***DefintionNode " + type_ + " is created***"

	def add_parameters(self, parameter):
		self.parameters.append(parameter)

	def __str__(self):
		return "Definition Node - Type: " + self.type_ + " ID: " + self.ID

class StatementNode(Node):
	"""StatementNode"""
	def __init__(self, type_):
		self.type_ = type_
		self.parameters = []
		print "***StatementNode " + type_ + " is created***"

	def add_parameters(self, parameter):
		self.parameters.append(parameter)

	def validate(self):
		pass
		# if type == "print":
		# 	if (args.type != string)
		# 		print "error"

	def evaulate_chain(obj):
		pass

	def __str__(self):
		return "Statement Node - Type: " + self.type_
