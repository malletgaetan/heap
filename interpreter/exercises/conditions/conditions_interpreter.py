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

# class CalcOp(AST):
#    def __init__(self, left, op, right):
#       self.left = left
#       self.right = right
#       self.op = op

# class ExprOp(AST):
#    def __init__(self, left, op, right):
#       # integer
#       self.left = left
#       # integer
#       self.right = right
#       # op
#       self.op = op

# class BoolOp(AST):
#    def __init__(self, left, op, right):
#       # bool
#       self.left = left
#       # bool
#       self.right = right
#       # comp
#       self.op = op

# class Boolean(AST):
#    def __init__(self, token):
#       self.token = token 

# class Integer(AST):
#    def __init__(self, value):
#       self.value = value



class Interpreter:
   def __init__(self, parser):
      self.parser = parser
   
   def visit_integer(self, node):
      return node.value

   def visit_boolean(self, node):
      if node.bool:
         return True if node.bool.type == Token.TRUE else False
      else:
         val = self.visit(node.node)
         return False if val == 0 else True

   def visit_calcop(self, node):
      a = self.visit(node.left)
      b = self.visit(node.right)
      if node.op.type == Token.MINUS:
         return a - b
      if node.op.type == Token.PLUS:
         return a + b

   def visit_exprop(self, node):
      a = self.visit(node.left)
      b = self.visit(node.right)
      if node.op.type == Token.LESS:
         return (a < b)
      if node.op.type == Token.LESS_EQUAL:
         return (a <= b)
      if node.op.type == Token.SUP:
         return (a > b)
      if node.op.type == Token.SUP_EQUAL:
         return (a >= b)
      if node.op.type == Token.EQUAL:
         return (a == b)
   
   def visit_boolop(self, node):
      a = self.visit(node.left)
      b = self.visit(node.right)
      if node.op.type == Token.AND:
         return (a and b)
      
      if node.op.type == Token.OR:
         return (a or b)

   def visit(self, node):
      if isinstance(node, Integer):
         return self.visit_integer(node)
      if isinstance(node, Boolean):
         return self.visit_boolean(node)
      if isinstance(node, CalcOp):
         return self.visit_calcop(node)
      if isinstance(node, BoolOp):
         return self.visit_boolop(node)
      if isinstance(node, ExprOp):
         return self.visit_exprop(node)

   def interpret(self):
      ast_node = self.parser.parse()
      return self.visit(ast_node)

def main():
   text = '((1 < 2) && ((True) && ((False) || (1 + 3 - 1 + 2 > 2))))'
   lexer = Lexer(input=text)
   parser = Parser(lexer=lexer)
   interpreter = Interpreter(parser=parser)
   # first version of conditions working! need some adjustement tho
   print(interpreter.interpret())

if __name__ == '__main__':
   main()