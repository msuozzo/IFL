import itertools

class CompilationException(Exception):
  def __init__(self, reason): self.reason = reason
  def __str__(self): return self.reason

class Program:
  def __init__(self, tree):
    self.tlts = [TLT(*tlt) for tlt in tree]
    self.tlt_names = [tlt.id_ for tlt in self.tlts]
    def_pairs = []
    for tlt in self.tlts: def_pairs.extend(tlt.get_add_fields())
    self.tlt_name_map = dict(zip(self.tlt_names, self.tlts))

    self.def_names = {}
    for name, id_and_type in def_pairs:
      id_ = id_and_type[0]
      self.def_names.setdefault(name, [])
      if id_ not in self.def_names[name]: self.def_names[name].append(id_)

    self.def_types = {}
    for tlt in self.tlts: self.def_types[tlt.id_] = tlt.type_
    for name, id_and_type in def_pairs:
      id_ = id_and_type[0]
      type_ = id_and_type[1]
      fullname = ".".join([name, id_])
      if type_ == TLT.UNKNOWN:
        try: type_ = self.tlt_name_map[id_].type_
        except KeyError:
          print id_
          print self.tlt_name_map
          raise CompilationException("non-tlt name added to object")
      if id_ in self.tlt_name_map and type_ != self.tlt_name_map[id_].type_:
        raise CompilationException("Duplicate name error")
      #FIX:possibility that 2 fields be added with same name but different type
      if fullname in self.def_types: 
        self.def_types[fullname] = None
        #TODO: warn that initiated with 2 different types
      else: self.def_types[fullname] = type_
    if "PLAYER" not in self.tlt_names: raise CompilationException("no PLAYER Character found")
    self.def_names.setdefault("PLAYER", [])
    self.def_types["PLAYER.LOCATION"] = "SETTING"
    self.def_names["PLAYER"].append("LOCATION")


  def validate_defs(self):
    for name, fields in self.def_names.iteritems():
      name_parts = name.split(".")
      if "LAST_INPUT" in name_parts + fields + self.tlt_names:
        raise CompilationException("improper use of reserved word LAST_INPUT")
      if "SELF" in name_parts and name_parts[0] != "SELF":
        raise CompilationException("SELF used as a non-root field")
      if "SELF" in fields + self.tlt_names:
        raise CompilationException("improper use of reserved word SELF")
      if "LOCATION" in self.tlt_names:
        raise CompilationException("improper use of reserved word LOCATION")
      if len(name_parts) == 1:
        if name_parts[0] not in self.tlt_names and name_parts[0] not in ["SELF", "LAST_INPUT", "LOCATION"]:
          raise CompilationException("invalid root object")
      if len(name_parts) > 1:
        previous = ".".join(name_parts[:-1])
        current = name_parts[-1]
        if previous not in self.def_names:
          raise CompilationException("invalid path")
        if current not in self.def_names[previous]:
          raise CompilationException("invalid path " + current + " never added to " + previous)


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
    self.actions = [Action(tup, self.id_) for tup in action[1]] if action else []
    self.functions = [Function(tup, self.id_) for tup in function[1]] if function else []
    self.dialogues = [Dialogue(tup, self.id_) for tup in dialogue[1]] if dialogue else []

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
    if self.dialogues:
      for dialogue in self.dialogues: ret.extend(dialogue.get_add_fields())
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
  EXIT="EXIT"

  def __init__(self, tup, tlt_name):
    tup = deep_sub_self(tup, tlt_name, [])
    self.type_ = tup[0]
    if self.type_ == Statement.ADD:
      self.primitive = None
      if isinstance(tup[2], tuple):
        self.primitive = Primitive(tup[2], tlt_name)
        self.id_ = self.primitive.name
      else: self.id_ = tup[2]
      self.quant = tup[1] if tup[1] else 1
      self.to = tup[3][1:]
    elif self.type_ == Statement.PRINT:
      self.string_exprs = tup[1]
    elif self.type_ == Statement.REMOVE:
      self.id_ = tup[2]
      self.quant = tup[1] if tup[1] else 1
      self.from_ = tup[3][1:]
    elif self.type_ == Statement.SET:
      self.target = tup[1][1:]
      self.val = tup[2]
    elif self.type_ == Statement.MOVE:
      self.target = tup[1][1:]
      self.new_loc = tup[2][1:]
    elif self.type_ == Statement.INCREASE:
      self.target = tup[1][1:]
      self.val = tup[2]
    elif self.type_ == Statement.DECREASE:
      self.target = tup[1][1:]
      self.val = tup[2]
    elif self.type_ == Statement.NUMBER:
      self.id_ = tup[1]
      self.target = tup[2][1:]
    elif self.type_ == Statement.INITIATE:
      self.label = tup[1]
    elif self.type_ == Statement.EXECUTE:
      self.func = tup[1][1:]
      self.args = tup[2]
    elif self.type_ == Statement.GOTO:
      self.label = tup[1]
    elif self.type_ == Statement.USING:
      self.filename = tup[1]
    elif self.type_ == Statement.EXIT: pass
    else: raise CompilationException("unrecognized type " + self.type_)

  def get_add_fields(self):
    if self.type_ == Statement.ADD:
      canonical_name = ".".join(self.to)
      datatype = self.primitive.type_ if self.primitive else TLT.UNKNOWN
      return [(canonical_name, (self.id_, datatype))]
    return []


class Conditional(Statement):
  def __init__(self, tup, tlt_name):
    tup = deep_sub_self(tup, tlt_name, [])
    # contains 2-tuples of (case, statement_list)
    self.cases = []
    for sec in tup[1:]:
      if not sec[1]: continue  #should activate on abscent ELSE clause
      case = sec[0]
      statements = [stat_or_cond(stat, tlt_name) for stat in sec[1]]
      self.cases.append((case, statements))
    self.possible_statements = list(itertools.chain.from_iterable([pair[1] for pair in self.cases]))
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
  def __init__(self, tup, tlt_name):
    self.type_ = tup[0]
    self.name = tup[1]
    self.val = tup[2]


class Dialogue:
  def __init__(self, tup, tlt_name):
    self.label = tup[0]
    self.statements = [stat_or_cond(stat, tlt_name) for stat in tup[1]]
    self.get_add_fields = lambda: get_add_fields(self.statements)


def gen_desc(type_, id_):
  return id_.capitalize() + " is a " + type_.capitalize()

def get_add_fields(lst):
  ret = []
  for elem in lst: ret.extend(elem.get_add_fields())
  return ret

def stat_or_cond(tup, tlt_name):
  return Conditional(tup, tlt_name) if tup[0] == "IF" else Statement(tup, tlt_name)

def deep_sub_self(lst, tlt_name, new_lst=[]):
  for elem in lst:
    if isinstance(elem, tuple):
      if len(elem) > 0 and elem[0] == "OBJ":
        tmp = [tlt_name if e=="SELF" else e for e in elem]
        if len(tmp) == 2 and tmp[1] == "LOCATION": tmp = [tmp[0], "PLAYER", tmp[1]]
        new_lst.append(tuple(tmp))
      else:
        new = []
        deep_sub_self(elem, tlt_name, new)
        new_lst.append(tuple(new))
    else: new_lst.append(elem)
  return tuple(new_lst)
