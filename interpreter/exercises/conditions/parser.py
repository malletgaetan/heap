from lexer import Token

class AST:
   pass

class CalcOp(AST):
   def __init__(self, left, op, right):
      self.left = left
      self.right = right
      self.op = op

class ExprOp(AST):
   def __init__(self, left, op, right):
      # integer
      self.left = left
      # integer
      self.right = right
      # op
      self.op = op

class BoolOp(AST):
   def __init__(self, left, op, right):
      # bool
      self.left = left
      # bool
      self.right = right
      # comp
      self.op = op

class Boolean(AST):
   def __init__(self, node=None, bool=None):
      self.node = node
      self.bool = bool

class Integer(AST):
   def __init__(self, value):
      self.value = value

class Parser:
   def __init__(self, lexer):
      self.lexer = lexer
      self.current_token = lexer.get_next_token()
   
   def advance(self, nb=1):
      for _ in range(nb):
         self.current_token = self.lexer.get_next_token()

   def eat(self, type):
      if self.current_token.type == type:
         return self.advance()
      raise Exception(f'expected {type} got {self.current_token.type}')

   # factor = INTEGER((PLUS|MINUS)INTEGER)*
   def factor(self):
      lastnode = Integer(value=self.current_token.value)
      self.eat(Token.INTEGER)
      while self.current_token.type in [Token.PLUS, Token.MINUS]:
         op = self.current_token
         # from PLUS|MINUS to INTEGER
         self.advance()
         lastnode = CalcOp(left=lastnode, op=op, right=Integer(value=self.current_token.value))
         # from INTEGER TO PLUS|MINUS
         self.advance()
      return lastnode

   # expr = factor(op factor)?
   def expr(self):
      left = self.factor()

      if self.current_token.type in [Token.LESS, Token.LESS_EQUAL, Token.SUP, Token.SUP_EQUAL, Token.EQUAL]:
         op = self.current_token
         self.advance()

         right = self.factor()
         return ExprOp(left=left, op=op, right=right)
      return Boolean(node=left)

   # boolean = FALSE | TRUE | expr
   def boolean(self):
      if self.current_token.type in [Token.FALSE, Token.TRUE]:
         bool = self.current_token
         self.advance()
         return Boolean(bool=bool)
      else:
         return self.expr()

   # cond = LPAREN boolean((AND|OR)cond)? RPAREN
   def cond(self):
      self.eat(Token.LPAREN)
      if self.current_token.type == Token.LPAREN:
         left = self.cond()
      else:
         left = self.boolean()
         self.eat(Token.RPAREN)
         # print('no its here')
      if self.current_token.type in [Token.AND, Token.OR]:
         op = self.current_token
         self.advance()
      else:
         return left
      right = self.cond()
      
      self.eat(Token.RPAREN)
      return BoolOp(left=left, op=op, right=right)

   def parse(self):
      return self.cond()