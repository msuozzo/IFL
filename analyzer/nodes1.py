import itertools
reserved_terms = (("SELF", ("LOCATION", "SETTING")),
                  )

class Program:
  def __init__(self, tree):
    self.tlts = [TLT(*tlt) for tlt in tree]
    self.tlt_names = [tlt.id_ for tlt in self.tlts]
    def_pairs = []
    for tlt in self.tlts:
      def_pairs.extend(tlt.get_add_fields())
    tlt_name_map = dict(zip(self.tlt_names, self.tlts))

    self.def_names = {}
    for name, id_and_type in def_pairs:
      id_ = id_and_type[0]
      self.def_names.setdefault(name, [])
      if id_ not in self.def_names[name]: self.def_names[name].append(id_)

    self.def_types = {}
    for name, id_and_type in def_pairs:
      id_ = id_and_type[0]
      type_ = id_and_type[1]
      fullname = ".".join([name, id_])
      if type_ == TLT.UNKNOWN:
        try: type_ = tlt_name_map[id_].type_
        except KeyError:
          raise Exception #TODO non-tlt name added to object 
      if id_ in tlt_name_map and type_ != tlt_name_map[id_].type_:
        raise Exception #TODO Duplicate name error
      #FIX:possibility that 2 fields be added with same name but different type
      if fullname in self.def_types: 
        self.def_types[fullname] = None
        #TODO: warn that initiated with 2 different types
      else: self.def_types[fullname] = type_

  def validate_defs(self):
    for name, fields in self.def_names.iteritems():
      name_parts = name.split(".")
      if "LAST_INPUT" in name_parts + fields + self.tlt_names:
        raise Exception #TODO improper use of reserved word LAST_INPUT
      if "SELF" in name_parts and name_parts[0] != "SELF":
        raise Exception #TODO SELF used as a non-root field
      if "SELF" in fields + self.tlt_names:
        raise Exception #TODO improper use of reserved word SELF
      if len(name_parts) == 1:
        if name_parts[0] not in self.tlt_names and name_parts[0] not in ["SELF", "LAST_INPUT"]:
          raise Exception #TODO invalid root object
      if len(name_parts) > 1:
        previous = ".".join(name_parts[:-1])
        current = name_parts[-1]
        if previous not in self.def_names:
          raise Exception #TODO invalid path
        if current not in self.def_names[previous]:
          raise Exception #TODO invalid path, current never added to previous


class TLT:
  TRAIT = "TRAIT"
  ITEM = "ITEM"
  CHARACTER = "CHARACTER"
  SETTING = "SETTING"
  UNKNOWN = "UNKNOWN"

  def __init__(self, type_, id_, desc, start, action=None, function=None, dialogue=None):
    self.type_ = type_
    self.id_ = id_
    self.desc = desc if desc is None else gen_desc(type_, id_)
    self.start = [stat_or_cond(tup, self.id_) for tup in start[1]]
    self.actions = [Action(tup, self.id_) for tup in action[1]] if action else None
    self.functions = [Function(tup, self.id_) for tup in function[1]] if function else None
    self.dialogue = Dialogue(dialogue, self.id_) if dialogue else None

  def gen_possible_fields(self):
    names = []
    for statement in self.start:
      names.extend(statement.get_add_fields())

  def get_add_fields(self):
    ret = []
    for stat in self.start: ret.extend(stat.get_add_fields())
    if self.actions:
      for action in self.actions: ret.extend(action.get_add_fields())
    if self.functions:
      for function in self.functions: ret.extend(function.get_add_fields())
    if self.dialogue: ret.extend(self.dialogue.get_add_fields())
    return ret


class Statement:
  ADD="ADD"
  PRINT="PRINT"
  REMOVE="REMOVE"
  SET="SET"
  MOVE="MOVE"
  INCREASE="INCREASE"
  DECREASE="DECREASE"
  NUMBER="NUMBER"
  INITIATE="INITIATE"
  EXECUTE="EXECUTE"
  GOTO="GOTO"
  USING="USING"

  def __init__(self, tup, tlt_name):
    self.type_ = tup[0]
    if self.type_ == Statement.ADD:
      self.primitive = None
      if isinstance(tup[2], tuple):
        self.primitive = Primitive(tup[2])
        self.id_ = self.primitive.name
      else: self.id_ = tup[2]
      self.quant = tup[1] if tup[1] else 1
      self.to = self_replace(tup[3], tlt_name)
    elif self.type_ == Statement.PRINT:
      self.string_expr = tup[1]
    elif self.type_ == Statement.REMOVE:
      self.id_ = tup[2]
      self.quant = tup[1] if tup[1] else 1
      self.from_ = self_replace(tup[3], tlt_name)
    elif self.type_ == Statement.SET:
      self.target = self_replace(tup[1], tlt_name)
      self.val = tup[2]
    elif self.type_ == Statement.MOVE:
      self.target = self_replace(tup[1], tlt_name)
      self.new_loc = tup[2]
    elif self.type_ == Statement.INCREASE:
      self.target = self_replace(tup[1], tlt_name)
      self.val = tup[2]
    elif self.type_ == Statement.DECREASE:
      self.target = self_replace(tup[1], tlt_name)
      self.val = tup[2]
    elif self.type_ == Statement.NUMBER:
      self.obj = tup[1]
      self.target = self_replace(tup[2], tlt_name)
    elif self.type_ == Statement.INITIATE:
      self.label = tup[1]
    elif self.type_ == Statement.EXECUTE:
      self.func = self_replace(tup[1], tlt_name)
      self.args = tup[2]
    elif self.type_ == Statement.GOTO:
      self.label = tup[1]
    elif self.type_ == Statement.USING:
      self.filename = tup[1]

  def get_add_fields(self):
    if self.type_ == Statement.ADD:
      canonical_name = ".".join(self.to)
      datatype = self.primitive.type_ if self.primitive else TLT.UNKNOWN
      return [(canonical_name, (self.id_, datatype))]
    return []


class Conditional(Statement):
  def __init__(self, tup, tlt_name):
    # contains 2-tuples of (case, statement_list)
    self.cases = []
    for sec in tup[1:]:
      if not sec[1]: continue  #should activate on abscent ELSE clause
      case = sec[0]
      statements = [stat_or_cond(stat, tlt_name) for stat in sec[1]]
      self.cases.append((case, statements))
    self.possible_statements = itertools.chain.from_iterable([pair[1] for pair in self.cases])
    self.get_add_fields = lambda: get_add_fields(self.possible_statements)


class Function:
  def __init__(self, tup, tlt_name):
    self.name = tup[0]
    self.arg_names = tup[1]
    self.statements = [stat_or_cond(stat, tlt_name) for stat in tup[2]]
    self.get_add_fields = lambda: get_add_fields(self.statements)
 

class Action:
  def __init__(self, tup, tlt_name):
    self.action_phrase = tup[0]
    self.statements = [stat_or_cond(stat, tlt_name) for stat in tup[1]]
    self.get_add_fields = lambda: get_add_fields(self.statements)


class Primitive:
  def __init__(self, tup):
    self.type_ = tup[0]
    self.name = tup[1]
    self.val = tup[2]


class Dialogue:
  def __init__(self, tup, tlt_name):
    self.label_map = {}
    for pair in tup[1:]:
      label = pair[0]
      statements = [stat_or_cond(stat, tlt_name) for stat in pair[1]]
      if label in self.label_map:
        raise Exception #TODO label used multiple times
      self.label_map[label] = statements
    self.labels = self.label_map.keys()
    self.all_statements = []
    for label, statements in self.label_map.iteritems():
      self.all_statements.extend(statements)
    self.get_add_fields = lambda: get_add_fields(self.all_statements)


def gen_desc(type_, id_):
  return id_.capitalize() + " is a " + type_.capitalize()

def get_add_fields(lst):
  ret = []
  for elem in lst: ret.extend(elem.get_add_fields())
  return ret

def stat_or_cond(tup, tlt_name):
  return Conditional(tup, tlt_name) if tup[0] == "IF" else Statement(tup, tlt_name)

def self_replace(lst, tlt_name):
  return [tlt_name if elem=="SELF" else elem for elem in lst[1:]]

