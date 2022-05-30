# exercise part 6
class Interpreter():
   def __init__(self, text):
      self.text = text
      self.pos = 0
      self.current_char = text[0]

   def to_next_token(self):
      text = self.text
      # move
      self.pos += 1

      # skip whitespaces
      while(self.pos < len(text) and text[self.pos].isspace()):
         self.pos += 1

      if self.pos >= len(text):
         self.current_char = None
         return

      self.current_char = text[self.pos]

   # factor=INTEGER|S_PARENTHESIS expr S_PARENTHESIS
   def factor(self):
      if self.current_char == '(':
         self.to_next_token()
         res = self.expr()
         self.to_next_token()
         return res
      if self.current_char.isdigit():
         current = self.current_char
         self.to_next_token()
         return int(current)

      raise Exception(f'expected either INTEGER or ( at position {self.pos} got {self.current_char}')

   # term=factor((PLUS|MINUS)factor)*
   def term(self):
      acc = self.factor()

      while(self.current_char is not None and self.current_char in '*/'):
         operator = self.current_char

         self.to_next_token()

         if operator == '*':
            acc *= self.factor()
         if operator == '/':
            acc /= self.factor()
         
      return acc

   # expr=term((PLUS|MINUS)term)*
   def expr(self):
      acc = self.term()

      while(self.current_char is not None and self.current_char in '+-'):
         operator = self.current_char

         self.to_next_token()

         if operator == '+':
            acc += self.term()
         if operator == '-':
            acc -= self.term()
      
      return acc

while True:
   calculus = input('calc> ')
   try:
      interpreter = Interpreter(calculus)
      result = interpreter.expr()
      print(result)
   except EOFError:
      break
   if not calculus:
      continue