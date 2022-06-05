class Token:
   EQUAL, SUP_EQUAL, LESS_EQUAL, SUP, LESS = ('==', '>=', '<=', '>', '<')
   FALSE, TRUE = ('FALSE', 'TRUE')
   LPAREN, RPAREN = ('(', ')')
   PLUS, MINUS = ('+', '-')
   OR, AND = ('||', '&&')
   INTEGER = 'EOF'
   EOF = 'EOF'
   def __init__(self, type, value):
      self.type = type
      self.value = value

class Lexer:
   def __init__(self, input):
      if len(input) == 0:
         raise Exception("input shouldn't be null")
      self.current_char = input[0]
      self.pos = 0
      self.text = input

   def advance(self, nb=1):
      self.pos += nb
      if self.pos >= len(self.text):
         self.current_char = None
         return
      self.current_char = self.text[self.pos]
   
   def skip_spaces(self):
      while self.current_char is not None and self.current_char.isspace():
         self.advance()

   def lex_integer(self):
      integer = ''
      while self.current_char is not None and self.current_char.isnumeric():
         integer += self.current_char
         self.advance()
      return int(integer)

   def get_next_token(self):
      self.skip_spaces()
      if self.current_char == None:
         return Token(Token.EOF, Token.EOF)

      if self.current_char.isnumeric():
         return Token(Token.INTEGER, self.lex_integer())

      current_char = self.current_char
      self.advance()

      if current_char.upper() == 'T':
         self.advance(3)
         return Token(Token.TRUE, Token.TRUE)

      if current_char.upper() == 'F':
         self.advance(4)
         return Token(Token.FALSE, Token.FALSE)

      if current_char == Token.LPAREN:
         return Token(Token.LPAREN, Token.LPAREN)

      if current_char == Token.PLUS:
         return Token(Token.PLUS, Token.PLUS)

      if current_char == Token.MINUS:
         return Token(Token.MINUS, Token.MINUS)

      if current_char == Token.RPAREN:
         return Token(Token.RPAREN, Token.RPAREN)

      if current_char == '=' and self.current_char == '=':
         return Token(Token.EQUAL, Token.EQUAL)

      if current_char == '>' and self.current_char == '=':
         self.advance()
         return Token(Token.SUP_EQUAL, Token.SUP_EQUAL)

      if current_char == Token.SUP:
         return Token(Token.SUP, Token.SUP)

      if current_char == '<' and self.current_char == '=':
         self.advance()
         return Token(Token.LESS_EQUAL, Token.LESS_EQUAL)

      if current_char == Token.LESS:
         return Token(Token.LESS, Token.LESS)

      if current_char == '|' and self.current_char == '|':
         self.advance()
         return Token(Token.OR, Token.OR)

      if current_char == '&' and self.current_char == '&':
         self.advance()
         return Token(Token.AND, Token.AND)
      

      raise Exception(f'unrecognized token {current_char} at pos {self.pos}')