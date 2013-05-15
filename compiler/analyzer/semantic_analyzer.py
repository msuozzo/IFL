from nodes import TLT, Statement, Program, Action, Function, Conditional, Dialogue, CompilationException
import sys

class Dummy: pass


def gen_tree(ast):
  try:
    prog = Program(ast)
    prog.validate_defs()
    type_check(prog, prog.def_types, prog.tlt_name_map)
  except CompilationException as e:
    print "="*10, "COMPILATION ERROR", "="*10
    print e.reason
    print "Terminating Compilation"
    sys.exit()
  return prog

def get_name(lst, type_map):
  try:
    return type_map[".".join(lst)]
  except:
    raise CompilationException("Name " + ".".join(lst) + " not found")

def type_check(stat, type_map, tlt_name_map):
  if isinstance(stat, Program):
    for tlt in stat.tlts: type_check(tlt, type_map, tlt_name_map)
  elif isinstance(stat, TLT):
    for start_stat in stat.start: type_check(start_stat, type_map, tlt_name_map)
    for action_stat in stat.actions: type_check(action_stat, type_map, tlt_name_map)
    for function_stat in stat.functions: type_check(function_stat, type_map, tlt_name_map)
    for dialogue_stat in stat.dialogues: type_check(dialogue_stat, type_map, tlt_name_map)
  elif isinstance(stat, Action):
    for stmt in stat.statements: type_check(stmt, type_map, tlt_name_map)
  elif isinstance(stat, Function):
    f_type_map = type_map
    for arg_name in stat.arg_names: f_type_map[arg_name] = None
    for stmt in stat.statements: type_check(stmt, f_type_map, tlt_name_map)
  elif isinstance(stat, Dialogue):
    for stmt in stat.statements: type_check(stmt, type_map, tlt_name_map)
  elif isinstance(stat, Conditional):
    for pair in stat.cases:
      case = pair[0]
      boolean_check(case, type_map)
    for stmt in stat.possible_statements: type_check(stmt, type_map, tlt_name_map)
  else: #Statements
    #print stat.type_
    if stat.type_ == Statement.ADD:
      if stat.primitive:
        prim_type = stat.primitive.type_
        if prim_type in ["INTEGER", "DECIMAL"]: arithmetic_check(stat.primitive.val, prim_type, type_map)
        elif prim_type == "BOOLEAN": boolean_check(stat.primitive.val, type_map)
        elif prim_type == "STRING": string_check(stat.primitive.val, type_map)
      else:
        if stat.quant <= 0: raise CompilationException("invalid quantity to add: " + stat.quant)
        target_type = get_name(stat.to, type_map)
        add_type = type_map[stat.id_]
        aggregation_check(target_type, add_type)
    elif stat.type_ == Statement.PRINT: print_string_check(stat.string_exprs, type_map)
    elif stat.type_ == Statement.REMOVE:
      if stat.quant <= 0: raise CompilationException("invalid quantity to remove: " + stat.quant)
      target_type = get_name(stat.from_, type_map)
      remove_type = type_map[stat.id_]
      aggregation_check(target_type, remove_type)

    elif stat.type_ == Statement.SET:
      target_type = get_name(stat.target, type_map)
      if target_type in ["INTEGER", "DECIMAL"]: arithmetic_check(stat.val, target_type, type_map)
      elif target_type == "STRING": string_check(stat.val, type_map)
      elif target_type == "TF": boolean_check(stat.val, type_map)
      else: raise CompilationException("attribute to be set must be a primitive")
    elif stat.type_ == Statement.MOVE:
      target_type = get_name(stat.target, type_map)
      loc_type = get_name(stat.new_loc, type_map)
      if target_type == "TRAIT": raise CompilationException("cannot move TRAIT")
      if loc_type != "SETTING": raise CompilationException("must move to setting")
    elif stat.type_ == Statement.INCREASE: #TODO COMBINE INCREASE AND DECREASE
      target_type = get_name(stat.target, type_map)
      int_fail, dec_fail = False, False
      if target_type == "INTEGER": 
        #print "ICREASE", stat.val
        try: arithmetic_check(stat.val, "INTEGER", type_map)
        except: int_fail = True
        try: arithmetic_check(stat.val, "DECIMAL", type_map)
        except: dec_fail = True
        #print stat.target
        #print int_fail, dec_fail
        if int_fail and dec_fail: raise CompilationException("cannot increase by non-numeric values")
        elif int_fail: raise CompilationException("cannot increase integer by a decimal amount")
      elif target_type == "DECIMAL":
        try: arithmetic_check(stat.val, "INTEGER", type_map)
        except: int_fail = True
        try: arithmetic_check(stat.val, "DECIMAL", type_map)
        except: dec_fail = True
        if int_fail and dec_fail: raise CompilationException("cannot increase by non-numeric values")
      else: raise CompilationException("can only increase numeric types")
    elif stat.type_ == Statement.DECREASE:
      target_type = get_name(stat.target, type_map)
      int_fail, dec_fail = False, False
      if target_type == "INTEGER": 
        try: arithmetic_check(stat.val, "INTEGER", type_map)
        except: int_fail = True
        try: arithmetic_check(stat.val, "DECIMAL", type_map)
        except: dec_fail = True
        if int_fail and dec_fail: raise CompilationException("cannot decrease by non-numeric values")
        elif int_fail: raise CompilationException("cannot decrease integer by a decimal amount")
      elif target_type == "DECIMAL":
        try: arithmetic_check(stat.val, "INTEGER", type_map)
        except: int_fail = True
        try: arithmetic_check(stat.val, "DECIMAL", type_map)
        except: dec_fail = True
        if int_fail and dec_fail: raise CompilationException("cannot decrease by non-numeric values")
      else: raise CompilationException("can only decrease numeric types")
    elif stat.type_ == Statement.NUMBER:
      target_type = get_name(stat.target, type_map)
      id_type = type_map[stat.id_]
      aggregation_check(target_type, id_type)
    elif stat.type_ == Statement.INITIATE: pass
    elif stat.type_ == Statement.EXECUTE:
      func_name = None
      try: func_name = stat.func[-2:]
      except: raise CompilationException("full path to function needed")
      stat.args = stat.args if stat.args else []
      expected_arguments = None
      for func in tlt_name_map[func_name[0]].functions:
        if func.name == func_name[1]:
          expected_arguments = len(func.arg_names)
          break
      if expected_arguments is None: raise CompilationException("function not found at path specified")
      if len(stat.args) != expected_arguments: raise CompilationException("incorrect number of arguments")
    elif stat.type_ == Statement.GOTO: pass
    elif stat.type_ == Statement.USING: pass


def aggregation_check(target_type, candidate_type):
  if not target_type: raise CompilationException("add target had duplicate types")
  if not candidate_type: raise CompilationException("action must be on TLT")
  if target_type == "CHARACTER":
    if candidate_type not in ["TRAIT", "ITEM"]: raise CompilationException("cannot add " + candidate_type + " to " + target_type)
  elif target_type == "SETTING":
    if candidate_type not in ["TRAIT", "ITEM", "CHARACTER"]: raise CompilationException("cannot add " + candidate_type + " to " + target_type)
  elif target_type == "TRAIT":
    if candidate_type not in ["ITEM"]: raise CompilationException("cannot add " + candidate_type + " to " + target_type)
  elif target_type == "ITEM": raise CompilationException("cannot add " + candidate_type + " to " + target_type)
  else: raise CompilationException("invalid target type " + target_type)

def boolean_check(stat, type_map):
  if stat in ['TRUE', 'FALSE']: pass
  #TODO maybe loose typechecking on Equals?
  elif stat[0] in ["==", "!="]: pass
  elif stat[0] in [">=", "<=", ">", "<"]:
    op = stat[0]
    int_fail, dec_fail = False, False
    name1 = get_dummy_name(stat[1])
    if not name1:
      try: arithmetic_check(stat[1], "INTEGER", type_map)
      except: int_fail = True
      try: arithmetic_check(stat[1], "DECIMAL", type_map)
      except: dec_fail = True
      if int_fail and dec_fail: raise CompilationException("cannot determine ordering of non-numeric values")
      elif not int_fail and not dec_fail: raise CompilationException("numeric type could not be determined")
    else:
      if get_name(stat[1][1:], type_map) not in ["INTEGER", "DECIMAL"]: raise CompilationException("cannot determine ordering of non-integral values")
    name2 = get_dummy_name(stat[2])
    if not name2:
      try: arithmetic_check(stat[2], "INTEGER", type_map)
      except: int_fail = True
      try: arithmetic_check(stat[2], "DECIMAL", type_map)
      except: dec_fail = True
      if int_fail and dec_fail: raise CompilationException("cannot determine ordering of non-integral values")
      elif not int_fail and not dec_fail: raise CompilationException("numeric type could not be determined")
      else: pass
    else:
      if get_name(stat[2][1:], type_map) not in ["INTEGER", "DECIMAL"]: raise CompilationException("cannot determine ordering of non-integral values")
  elif stat[0] == "HAS":
    target_type = get_name(stat[1][1:], type_map)
    has_type = type_map[stat[2]]
    aggregation_check(target_type, has_type)
    if not target_type: raise CompilationException("add target had duplicate types")
    if not has_type: raise CompilationException("add must be TLT")
    if target_type == "CHARACTER":
      if has_type not in ["TRAIT", "ITEM"]: raise CompilationException("cannot add " + has_type + " to " + target_type)
    elif target_type == "SETTING":
      if has_type not in ["TRAIT", "ITEM", "CHARACTER"]: raise CompilationException("cannot add " + has_type + " to " + target_type)
    elif target_type == "TRAIT":
      if has_type not in ["ITEM"]: raise CompilationException("cannot add " + has_type + " to " + target_type)
    elif target_type == "ITEM": raise CompilationException("cannot add " + has_type + " to " + target_type)
    else: raise CompilationException("invalid target type " + target_type)
  elif stat[0] == "NOT": boolean_check(stat[1], type_map)
  elif stat[0] == "(": boolean_check(stat[1], type_map)
  elif stat[0] in ["OR", "AND"]:
    op = stat[0]
    int_fail, dec_fail = False, False
    if get_dummy_name(stat[1]):
      if get_name(stat[1][1:], type_map) != "TF": raise CompilationException("non-true/false used in and/or expression")
    else: boolean_check(stat[1], type_map)
    if get_dummy_name(stat[2]):
      if get_name(stat[2][1:], type_map) != "TF": raise CompilationException("non-true/false used in and/or expression")
    else: boolean_check(stat[2], type_map)
  else:
    print stat
    raise CompilationException("invalid formation of boolean statement")

def string_check(stat, type_map):
  obj_list = []
  for expr in stat:
    if isinstance(expr, str): pass
    elif expr[0] == "OBJ": obj_list.append(".".join(expr[1:]))
    else: raise CompilationException("invalid string")
  for obj_name in obj_list:
    if type_map[obj_name] not in ["STRING", None]: raise CompilationException(obj_name + " not of type " + target_type)

def print_string_check(stat, type_map):
  obj_list = []
  for expr in stat:
    if expr in ["TRUE", "FALSE"]: pass #cmd_list.append(expr)
    elif expr[0] == "LIT": pass #cmd_list.append(str(expr[1]))
    elif expr[0] == "OBJ": obj_list.append(".".join(expr[1:]))
    else:
      if not isinstance(expr, str): raise CompilationException("invalid print string")
      pass #cmd_list.append(expr)
  for obj_name in obj_list:
    if type_map[obj_name] not in ["STRING", "INTEGER", "DECIMAL", "TF", None]: raise CompilationException(obj_name + " not of type " + target_type)

def arithmetic_check(stat, target_type, type_map):
  obj_list, cmd_list = [], []
  arithmetic_sub(stat, obj_list, cmd_list)
  for obj in obj_list:
    obj_name = obj.split(".", 1)[1]
    if type_map[obj_name] not in [target_type, None]: raise CompilationException(obj_name + " not of type " + target_type)
  a_dummy = Dummy()
  for obj in obj_list:
    curr = "a_dummy"
    split_lst = obj.split(".")
    for lvl in split_lst[1:-1]:
      curr += "." + lvl
      exec(curr + " = Dummy()")
    obj_name = obj.split(".", 1)[1]
    if type_map[obj_name] not in [target_type, None]: raise CompilationException(obj_name +  " not of type " + target_type)
    val = 1 if target_type == "INTEGER" else 1.0
    exec("setattr("+curr+",'"+split_lst[-1]+"',"+str(val)+")")
  for cmd in cmd_list:
    try:
      #print cmd
      res = eval(cmd)
      #print "res", res, isinstance(res, int), target_type
      py_type = int if target_type == "INTEGER" else float
      if not isinstance(res, py_type): raise CompilationException("resolved expression not of target type")
    except ZeroDivisionError: pass #TODO WARNING: Possible division by zero detected

get_dummy_name = lambda obj: "a_dummy."+".".join(obj[1:]) if obj[0] == "OBJ" else None
def arithmetic_sub(stat, obj_list, cmd_list):
#  if stat == ('LIT', '1.0'): import pdb; pdb.set_trace()
  if stat[0] in ["+", "%", "/", "*", "^"] or (stat[0] == "-" and len(stat) == 3):
    op = "**" if stat[0] == "^" else stat[0]
    arg1, arg2 = None, None
    name1 = get_dummy_name(stat[1])
    if name1:
      obj_list.append(name1)
      arg1 = name1
      cmd_list.append(name1)
    else: arg1 = arithmetic_sub(stat[1], obj_list, cmd_list)
    name2 = get_dummy_name(stat[2])
    if name2:
      obj_list.append(name2)
      arg2 = name2
      cmd_list.append(name2)
    else: arg2 = arithmetic_sub(stat[2], obj_list, cmd_list)
    cmd = "("+str(arg1)+")"+op+"("+str(arg2)+")"
    cmd_list.append(cmd)
    return cmd
  elif stat[0] == "-": #unary
    name = get_dummy_name(stat[1])
    if name: obj_list.append(name)
    arg1 = arithmetic_sub(stat[1], obj_list, cmd_list)
    cmd = "(-1*"+str(arg1)+")"
    cmd_list.append(cmd)
    return cmd
  elif stat[0] == "LIT":
    cmd = "("+stat[1]+")"
    cmd_list.append(cmd)
    return cmd
  elif stat[0] == "OBJ":
    name = get_dummy_name(stat)
    obj_list.append(name)
    cmd = "("+str(name)+")"
    cmd_list.append(cmd)
    return cmd
  elif stat[0] == "(":
    arg1 = arithmetic_sub(stat[1], obj_list, cmd_list)
    cmd = "("+str(arg1)+")"
    cmd_list.append(cmd)
    return cmd
  elif isinstance(stat, tuple) and len(stat) == 1:
    return str(arithmetic_sub(stat[0], obj_list, cmd_list))
  else:
    print stat
    print "boo"
    raise Exception

