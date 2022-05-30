# pos should be equal to the current pos of pointer
def get_next_character(text, pos):
   if pos is None:
      pos = 0
   else:
      pos += 1
   while(pos < len(text) and text[pos].isspace()):
      pos += 1
   if pos >= len(text):
      return None, pos
   return text[pos], pos

def test_integer(character, pos):
   if character is None or not character.isdigit():
      raise Exception(f'expected a single digit integer at pos {pos + 1} got {character}')

def future(calculus, pos):
   current_char, pos = get_next_character(calculus, pos)
   if current_char == '(':
      return calc(calculus, pos)
   test_integer(current_char, pos)
   return int(current_char), current_char, pos

def mult_div(calculus, pos):
   # can get either ( or INTEGER
   acc, current_char, pos = future(calculus, pos)
   # can get either DIVIDE or MULTIPLY
   current_char, pos = get_next_character(calculus, pos)
   while(current_char is not None and current_char in '*/'):
      operator = current_char

      if operator == '*':
         res, current_char, pos = future(calculus, pos)
         acc *= res
      if operator == '/':
         res, current_char, pos = future(calculus, pos)
         acc /= res

      current_char, pos = get_next_character(calculus, pos)

   return acc, current_char, pos

# take a string of addition and soustration, interpet it and give result
def calc(calculus, pos = None):
   # can get either ( or INTEGER
   acc, current_char, pos = mult_div(calculus, pos)
   # can get either PLUS or MINUS
   while(current_char is not None and current_char != ')' and current_char in '+-'):
      # current_char should be an operator
      operator = current_char
      
      # pos here is pointing either to an INTEGER or an OPENED PARENTHESIS
      if operator == '-':
         res, current_char, pos = mult_div(calculus, pos)
         acc -= res
      if operator == '+':
         res, current_char, pos = mult_div(calculus, pos)
         acc += res

      print(f'after={current_char}')

   return acc, current_char, pos

while True:
   calculus = input('calc> ')
   try:
      res, _, _ = calc(calculus)
      print(res)
   except EOFError:
      break
   if not calculus:
      continue