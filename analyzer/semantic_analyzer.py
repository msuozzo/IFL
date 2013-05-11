from nodes1 import TLT, Statement, Program

class Dummy: pass


def gen_tree(ast):
  prog = Program(ast)
  prog.validate_defs()
  return prog
  type_check(prog)
  #if prog.def_types[]
  import sys; sys.exit()

def type_check(stat):
  if isinstance(stat, Program):
    for tlt in stat.tlts: type_check(tlt)
  elif isinstance(stat, TLT):
    for start_stat in stat.start: type_check(start_stat)
    for action_stat in stat.actions: type_check(action_stat)
    for function_stat in stat.functions: type_check(function_stat)
    for dialogue_stat in stat.dialogues: type_check(dialogue_stat)
  elif isinstance(stat, Action):
    for tlt in stat.start: type_check(tlt)
  elif isinstance(stat, Function):
    for tlt in stat.start: type_check(tlt)
  elif isinstance(stat, Dialogue):
    for tlt in stat.start: type_check(tlt)
  if stat.type_ == Statement.ADD:
    if stat.primitive:
      pass
#      stat.primitive.type_ == 
  elif self.type_ == Statement.PRINT:
    pass
  elif self.type_ == Statement.REMOVE:
    pass
  elif self.type_ == Statement.SET:
    pass
  elif self.type_ == Statement.MOVE:
    pass
  elif self.type_ == Statement.INCREASE:
    pass
  elif self.type_ == Statement.DECREASE:
    pass
  elif self.type_ == Statement.NUMBER:
    pass
  elif self.type_ == Statement.INITIATE:
    pass
  elif self.type_ == Statement.EXECUTE:
    pass
  elif self.type_ == Statement.GOTO:
    pass
  elif self.type_ == Statement.USING:
    pass


get_dummy_name = lambda obj: "a_dummy."+".".join(obj[1:]) if obj[0] == "OBJ" else None
def arithmetic_sub(stat, obj_list, cmd_list):
  if stat[0] in ["+", "%", "/", "*", "^"] or \
    (stat[0] == "-" and len(stat) == 3):
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
  else:
    print stat
    raise Exception

x = []
cmds = []
stat = ('-', ('+', ('OBJ', 'health', 'current'), ('LIT', '50')), ('OBJ', 'PLAYER', 'pops'))
print arithmetic_sub(stat, x, cmds), x
print cmds

