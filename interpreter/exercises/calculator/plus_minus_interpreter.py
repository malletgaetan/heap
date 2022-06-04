# pos should be equal to the current pos of pointer
def get_next_character(text, pos):
   if pos is None:
      pos = 0
   else:
      pos += 1
   while(pos < len(text) and text[pos].isspace()):
      pos += 1
   if len(text) == pos:
      return None, pos
   return text[pos], pos 

# take a string of addition and soustration, interpet it and give result
def calc(calculus):
   pos = None
   current_char, pos = get_next_character(calculus, pos)
   if not current_char.isdigit():
      raise Exception('calculus should start by a single digit integer')
   acc = int(current_char)
   current_char, pos = get_next_character(calculus, pos)
   while(current_char is not None):
      # current_char should be an operator
      if current_char not in '+-':
         raise Exception(f'expected operator at pos {pos + 1}')
      operator = current_char

      # current_char should be an single digit integer 
      current_char, pos = get_next_character(calculus, pos)
      if not current_char.isdigit():
         raise Exception(f'expected a single digit integer at pos {pos + 1}')
      if operator == '-':
         acc -= int(current_char)
      if operator == '+':
         acc += int(current_char)
      
      current_char, pos = get_next_character(calculus, pos)

   return acc

while True:
   calculus = input('calc> ')
   try:
      print(calc(calculus))
   except EOFError:
      break
   if not calculus:
      continue