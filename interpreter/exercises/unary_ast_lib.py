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

class ArithmeticOp:
   def __init__(self, left, op, right):
      self.left = left
      self.op = op
      self.right = right

class Integer:
   def __init__(self, token):
      self.token = token
      self.value = token.value

class UnaryOp:
   def __init__(self, op, expr):
      self.op = op
      self.expr = expr


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

   # factor=(PLUS|MINUS)factor|Token.INTEGER|(Token.LPAREN Token.INTEGER Token.RPAREN)
   def factor(self):
      token = self.token
      if token.type == Token.PLUS:
         self.eat(Token.PLUS)
         return UnaryOp(op=token, expr=self.factor())
      if token.type == Token.MINUS:
         self.eat(Token.MINUS)
         return UnaryOp(op=token, expr=self.factor())
      if token.type == Token.LPAREN:
         self.next_token() 
         op = self.expr()
         self.eat(Token.RPAREN)
         return op
      if token.type == Token.INTEGER:
         self.next_token() 
         return Integer(token=token)

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

         lastop = ArithmeticOp(left=lastop, op=operator, right=self.factor())
      
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

         lastop = ArithmeticOp(left=lastop, op=operator, right=self.term())
      
      return lastop

   def parse(self):
      return self.expr()

class Interpreter:
   def __init__(self, parser):
      self.parser = parser

   def visit_binop(self, node):
      if node.op.type == Token.PLUS:
         return self.visit(node.left) + self.visit(node.right)
      elif node.op.type == Token.MINUS:
         return self.visit(node.left) - self.visit(node.right)
      elif node.op.type == Token.MUL:
         return self.visit(node.left) * self.visit(node.right)
      elif node.op.type == Token.DIV:
         return self.visit(node.left) // self.visit(node.right)

   def visit_integer(self, node):
      return node.value

   def visit_unaryop(self, node):
      op = node.op.type
      if op == Token.PLUS:
         return +self.visit(node.expr)
      elif op == Token.MINUS:
         return -self.visit(node.expr)

   def visit(self, node):
      if isinstance(node, ArithmeticOp):
         return self.visit_binop(node)
      if isinstance(node, Integer):
         return self.visit_integer(node)
      if isinstance(node, UnaryOp):
         return self.visit_unaryop(node)
      raise Exception('unknown AST node type')

   def interpret(self):
      tree = self.parser.parse()
      result = self.visit(tree)
      return result