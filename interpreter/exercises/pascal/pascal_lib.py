class Token:
   EOF, INTEGER, LPAREN, RPAREN, PLUS, MINUS, DIV, MUL = ('EOF', 'INTEGER', '(', ')', '+', '-', '/', '*')
   DOT, ID, ASSIGNEMENT, SEMI, EMPTY = ('.', 'ID', ':=', ';', 'EMPTY')
   BEGIN, END = ('BEGIN', 'END')

   def __init__(self, type, value):
      self.type = type
      self.value = value


class Lexer:
   RESERVED_KEYWORDS = {
      'BEGIN': Token(Token.BEGIN, Token.BEGIN),
      'END': Token(Token.END, Token.END)
   }

   def __init__(self, program):
      self.program = program
      self.current_char = self.program[0]
      self.pos = 0

   def advance(self):
      self.pos += 1
      if self.pos > len(self.program) - 1:
         self.current_char = None
      else:
         self.current_char = self.program[self.pos]
   
   def peek(self):
      pos = self.pos + 1
      while self.program[pos] is not None and self.program[pos].isspace():
         pos += 1
      return self.program[pos]

   def skip_spaces(self):
      while(self.current_char is not None and self.current_char.isspace()):
         self.advance()
   
   def lex_id(self):
      result = ''
      while self.current_char is not None and self.current_char.isalnum():
         result += self.current_char
         self.advance()
      return Lexer.RESERVED_KEYWORDS.get(result, Token(Token.ID, result))

   def lex_integer(self):
      integer = ""
      while(self.current_char != None and self.current_char.isdigit()):
         integer += self.current_char
         self.advance()
      return int(integer)
   
   def get_next_token(self):
      self.skip_spaces()
      while self.current_char is not None:
         # either variable declaration or keyword
         if self.current_char.isalpha():
            return self.lex_id()

         if self.current_char == ':' and self.peek() == '=':
            self.advance()
            self.advance()
            return Token(Token.ASSIGNEMENT, Token.ASSIGNEMENT)

         if self.current_char == '.':
            self.advance()
            return Token(Token.DOT, Token.DOT)

         if self.current_char == ';':
            self.advance()
            return Token(Token.SEMI, Token.SEMI)

         if self.current_char.isdigit():
            return Token(Token.INTEGER, self.lex_integer())

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


# parse type
class AST:
   pass

class BinOp(AST):
   def __init__(self, left, op, right):
      self.left = left
      self.op = op
      self.right = right

class Integer(AST):
   def __init__(self, token):
      self.token = token
      self.value = token.value

class UnaryOp(AST):
   def __init__(self, op, expr):
      self.op = op
      self.expr = expr

class AssignOp(AST):
   def __init__(self, left, op, right):
      self.left = left
      self.right = right 
      self.op = op 

class Compound(AST):
   def __init__(self, childrens):
      self.childrens = childrens

class NoOp(AST):
   pass

class Var(AST):
   def __init__(self, token):
      self.token = token
      self.name = token.value

# Grammar rules
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

   def variable(self):
      node = Var(self.token)
      self.eat(Token.ID)
      return node

   # factor=(PLUS|MINUS)factor|Token.INTEGER|(Token.LPAREN Token.INTEGER Token.RPAREN)|variable
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
      if token.type == Token.ID:
         return self.variable()

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

         lastop = BinOp(left=lastop, op=operator, right=self.factor())
      
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

         lastop = BinOp(left=lastop, op=operator, right=self.term())
      
      return lastop

   # empty
   def empty(self):
      return NoOp()

   # assignment_statement : variable ASSIGN expr
   def assignement_statement(self):
      left = self.variable()
      op = self.token
      self.eat(Token.ASSIGNEMENT)
      right = self.expr()
      return AssignOp(left=left, op=op, right=right)

   # statement : compound_statement | assignment_statement | empty
   def statement(self):
      # compound_statement
      if self.token.type == Token.BEGIN:
         return self.compound_statement()
      # assignment_statement
      elif self.token.type == Token.ID:
         return self.assignement_statement()
      # empty
      else:
         return self.empty()

   # statement_list : statement | statement SEMI statement_list
   def statement_list(self):
      statement = self.statement()
      statements = [statement]
      while self.token.type == Token.SEMI:
         self.eat(Token.SEMI)
         statements.append(self.statement())
      return statements 

   # compound_statement : BEGIN statement_list END
   def compound_statement(self):
      self.eat(Token.BEGIN)
      node = self.statement_list()
      self.eat(Token.END)
      return Compound(childrens=node)

   # program : compound_statement DOT
   def program(self):
      compound = self.compound_statement()
      self.eat(Token.DOT)
      return compound

   def parse(self):
      return self.program()

class Interpreter:
   def __init__(self, parser):
      self.parser = parser
      self.GLOBAL_SCOPE = {}

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

   def visit_assignop(self, node):
      var_name = node.left.name
      self.GLOBAL_SCOPE[var_name] = self.visit(node.right)

   def visit_var(self, node):
      name = node.name
      value = self.GLOBAL_SCOPE.get(name, None)
      return value

   def visit_compound(self, node):
      for child in node.childrens:
         if isinstance(child, AssignOp):
            self.visit_assignop(child)
         if isinstance(child, Compound):
            self.visit_compound(child)

   def visit(self, node):
      if isinstance(node, BinOp):
         return self.visit_binop(node)
      if isinstance(node, Integer):
         return self.visit_integer(node)
      if isinstance(node, UnaryOp):
         return self.visit_unaryop(node)
      if isinstance(node, Compound):
         return self.visit_compound(node)
      if isinstance(node, Var):
         return self.visit_var(node)
      if isinstance(node, AssignOp):
         return self.visit_assignop(node)
      raise Exception('unknown AST node type')

   def interpret(self):
      tree = self.parser.parse()
      self.visit(tree)
      return tree