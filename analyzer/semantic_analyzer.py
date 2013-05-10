from nodes1 import TLT, Statement, Program

class Dummy: pass


def gen_tree(ast):
  prog = Program(ast)
  prog.validate_defs()
  return prog
  import sys; sys.exit()

def type_check(stat):
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
def arithmetic_sub(stat, obj_list):
  if stat[0] in ["+", "%", "/", "*", "^"]:
    op = "**" if stat[1] == "^" else stat[1]
    name = get_dummy_name(stat[1])
    if name: obj_list.append(name)
    name = get_dummy_name(stat[2])
    if name: obj_list.append(name)
    arg1 = arithmetic_sub(stat[1], obj_list)
    arg2 = arithmetic_sub(stat[2], obj_list)
    return "("+str(arg1)+")"+op+"("+str(arg2)+")"
  elif stat[0] == "-":
    pass
  elif stat[0] == "LIT":
    pass
  else:
    pass


