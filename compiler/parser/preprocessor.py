

def clean_input(data):
  end_block = "END_BLOCK"
  fixed_lines = []
  last = 0
  for line in data.splitlines():
    if not line.strip(): continue
    curr = 0
    for char in line:
      if char == '\t': curr += 1
      else: break
    while curr < last:
      fixed_lines.append(end_block)
      last -= 1
    last = curr
    if line[-1] == ':': last += 1
    fixed_lines.append(line.strip())
  while last > 0:
    fixed_lines.append(end_block)
    last -= 1
  return fixed_lines



