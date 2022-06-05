class Token:
   EOF, INTEGER, LPAREN, RPAREN, PLUS, MINUS, DIV, MUL = ('EOF', 'INTEGER', '(', ')', '+', '-', '/', '*')
   def __init__(self, type, value):
      self.type = type
      self.value = value


class Lexer:
   def __init__(self, calculus):
      self.calculus = calculus
      self.current_char = calculus[0]
      self.pos = 0

   def advance(self):
      self.pos += 1
      if self.pos > len(self.calculus) - 1:
         self.current_char = None
      else:
         self.current_char = self.calculus[self.pos]

   def skip_spaces(self):
      while(self.current_char is not None and self.current_char.isspace()):
         self.advance()

   def parseInteger(self):
      integer = ""
      while(self.current_char != None and self.current_char.isdigit()):
         integer += self.current_char
         self.advance()
      return int(integer)
   
   def get_next_token(self):
      self.skip_spaces()
      while self.current_char is not None:
         if self.current_char.isdigit():
            return Token(Token.INTEGER, self.parseInteger())

         if self.current_char == Token.PLUS:
            self.advance()
            return Token(Token.PLUS, Token.PLUS)

         if self.current_char == Token.MINUS:
            self.advance()
            return Token(Token.MINUS, Token.MINUS)

         if self.current_char == Token.DIV:
            self.advance()
            return Token(Token.DIV, Token.DIV)

         if self.current_char == Token.MUL:
            self.advance()
            return Token(Token.MUL, Token.MUL)

         if self.current_char == Token.LPAREN:
            self.advance()
            return Token(Token.LPAREN, Token.LPAREN)

         if self.current_char == Token.RPAREN:
            self.advance()
            return Token(Token.RPAREN, Token.RPAREN)
         
         raise Exception(f'unrecognized token {self.current_char}')

      return Token(Token.EOF, None)

class ASTOp:
   def __init__(self, left, operator, right):
      self.left = left
      self.operator = operator
      self.right = right

class ASTNum:
   def __init__(self, token):
      self.token = token
      self.value = token.value


# expr=term((Token.PLUS|Token.MINUS)term)*
# term=factor((Token.DIV|Token.MUL)factor)*
# factor=Token.INTEGER|(Token.LPAREN Token.INTEGER Token.RPAREN)
class Parser:
   def __init__(self, lexer: Lexer):
      self.lexer = lexer
      self.token = self.lexer.get_next_token()

   def next_token(self):
      self.token = self.lexer.get_next_token()

   def eat(self, type):
      if not self.token.type == type:
         raise Exception(f'expected {type}, got {self.token.type}')
      self.next_token()

   # factor=Token.INTEGER|(Token.LPAREN Token.INTEGER Token.RPAREN)
   def factor(self):
      if self.token.type == Token.LPAREN:
         self.next_token() 
         op = self.expr()
         self.eat(Token.RPAREN)
         return op

      if self.token.type == Token.INTEGER:
         num = self.token
         self.next_token() 
         return ASTNum(token=num)

      raise Exception(f'expected {Token.LPAREN} or {Token.INTEGER}, got {self.token.type}')
   
   # term=factor((Token.DIV|Token.MUL)factor)*
   def term(self):
      lastop = self.factor()

      while self.token.type in [Token.DIV, Token.MUL]:
         operator = self.token

         if operator.type == Token.DIV:
            self.eat(Token.DIV)
         if operator.type == Token.MUL:
            self.eat(Token.MUL)

         lastop = ASTOp(left=lastop, operator=operator, right=self.factor())
      
      return lastop
   
   # expr=term((Token.PLUS|Token.MINUS)term)*
   def expr(self):
      lastop = self.term()

      while self.token.type in [Token.PLUS, Token.MINUS]:
         operator = self.token

         if operator.type == Token.PLUS:
            self.eat(Token.PLUS)
         if operator.type == Token.MINUS:
            self.eat(Token.MINUS)

         lastop = ASTOp(left=lastop, operator=operator, right=self.term())
      
      return lastop

   def parse(self):
      return self.expr()
