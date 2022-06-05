class Token:
   EOF, INTEGER, REAL, LPAREN, RPAREN, PLUS, MINUS, FLOAT_DIV, MUL = ('EOF', 'INTEGER', 'REAL', '(', ')', '+', '-', '/', '*')
   DOT, ID, ASSIGNEMENT, SEMI, EMPTY, DECL_SEP, VAR, DECL = ('.', 'ID', ':=', ';', 'EMPTY', ',', 'VAR', ':')
   BEGIN, END, INTEGER_DIV, PROGRAM, COMMENT_START, COMMENT_END = ('BEGIN', 'END', 'DIV', 'PROGRAM', '{', '}')

   def __init__(self, type, value):
      self.type = type
      self.value = value


class Lexer:
   RESERVED_KEYWORDS = {
      'BEGIN': Token(Token.BEGIN, Token.BEGIN),
      'END': Token(Token.END, Token.END),
      'DIV': Token(Token.INTEGER_DIV, Token.INTEGER_DIV),
      'PROGRAM': Token(Token.PROGRAM, Token.PROGRAM),
      'VAR': Token(Token.VAR, Token.VAR),
      'INTEGER': Token(Token.INTEGER, Token.INTEGER),
      'REAL': Token(Token.REAL, Token.REAL)
   }

   def __init__(self, program):
      self.program = program
      self.current_char = self.program[0]
      self.pos = 0

   def advance(self, nb=1):
      self.pos += nb
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
      result = self.current_char
      self.advance()
      while self.current_char is not None and self.current_char.isalnum():
         result += self.current_char
         self.advance()
      result = result.upper()
      return Lexer.RESERVED_KEYWORDS.get(result, Token(Token.ID, result))
   
   # can optimize this
   def lex_number(self):
      number = ''
      while self.current_char != None and (self.current_char.isdigit() or self.current_char == '.'):
         number += self.current_char
         self.advance()
      if '.' in number:
         return Token(Token.REAL, float(number))
      return Token(Token.INTEGER, int(number))
   
   def skip_comment(self):
      while self.current_char != Token.COMMENT_END:
         self.advance()
      self.advance()
   
   def get_next_token(self):
      self.skip_spaces()
      while self.current_char is not None:
         if self.current_char == Token.COMMENT_START:
            self.skip_comment()
            return self.get_next_token()

         if self.current_char == ',':
            self.advance()
            return Token(Token.DECL_SEP, Token.DECL_SEP)

         # variable or keyword
         if self.current_char.isalpha() or self.current_char == '_':
            return self.lex_id()

         if self.current_char == ':':
            if self.peek() == '=':
               self.advance(2)
               return Token(Token.ASSIGNEMENT, Token.ASSIGNEMENT)

            self.advance()
            return Token(Token.DECL, Token.DECL)

         if self.current_char == '.':
            self.advance()
            return Token(Token.DOT, Token.DOT)

         if self.current_char == ';':
            self.advance()
            return Token(Token.SEMI, Token.SEMI)

         if self.current_char.isdigit():
            # INTEGER | REAL
            return self.lex_number()

         if self.current_char == Token.PLUS:
            self.advance()
            return Token(Token.PLUS, Token.PLUS)

         if self.current_char == Token.MINUS:
            self.advance()
            return Token(Token.MINUS, Token.MINUS)

         if self.current_char == Token.FLOAT_DIV:
            self.advance()
            return Token(Token.FLOAT_DIV, Token.FLOAT_DIV)

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

      return Token(Token.EOF, Token.EOF)

# parse type
class AST:
   pass

class BinOp(AST):
   def __init__(self, left, op, right):
      self.left = left
      self.op = op
      self.right = right

class Number(AST):
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

# isn't actually used, isn't needed for the moment
class NoOp(AST):
   pass

class VarDecl(AST):
   def __init__(self, variable, type):
      self.var_node = variable
      self.type_node = type

class Block(AST):
   def __init__(self, declarations, compound):
      self.declarations = declarations
      self.compound = compound

class Program(AST):
   def __init__(self, name, block):
      self.name = name
      self.block_node = block

class Type(AST):
   def __init__(self, token):
      self.token = token
      self.value = token.value

# class DeclareOp(AST):
#    def __init__(self, variable, type):
#       self.variable = variable
#       self.type = type

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

   # variable = ID
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
         return Number(token=token)
      if token.type == Token.REAL:
         self.next_token()
         return Number(token=token)
      if token.type == Token.ID:
         return self.variable()

      raise Exception(f'expected {Token.LPAREN} or {Token.INTEGER}, got {self.token.type}')
   
   # term=factor((Token.DIV|Token.MUL)factor)*
   def term(self):
      lastop = self.factor()

      while self.token.type in [Token.FLOAT_DIV, Token.MUL, Token.INTEGER_DIV]:
         operator = self.token

         if operator.type == Token.MUL:
            self.eat(Token.MUL)
         if operator.type == Token.INTEGER_DIV:
            self.eat(Token.INTEGER_DIV)
         if operator.type == Token.FLOAT_DIV:
            self.eat(Token.FLOAT_DIV)

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

   # type: INTEGER | REAL
   def type(self):
      node = Type(self.token)
      if self.token.type == Token.INTEGER:
         self.eat(Token.INTEGER)
      if self.token.type == Token.REAL:
         self.eat(Token.REAL)
      return node

   #declaration: variable(DECL_SEP variable)* DECL TYPE
   def declaration(self):
      variable = self.variable()
      variables = [variable]
      while self.token.type == Token.DECL_SEP:
         self.eat(Token.DECL_SEP)
         variables.append(self.variable())
      
      self.eat(Token.DECL)

      type = self.type()

      return [VarDecl(variable=variable, type=type) for variable in variables]

   # variables_declaration: VAR (declaration DECL_SEP)+ | empty
   def variables_declaration(self):
      self.eat(Token.VAR)
      
      # empty var declaration
      if self.token.type == Token.BEGIN:
         return []

      declarations = []
      while declaration := self.declaration():
         declarations += declaration
         self.eat(Token.SEMI)
         if self.token.type == Token.BEGIN:
            break

      return declarations

   # block : variables_declaration compound_statement
   def block(self):
      variables_declaration = self.variables_declaration()
      compound = self.compound_statement()
      return Block(declarations=variables_declaration, compound=compound)

   # program : PROGRAM variable SEMI block DOT
   def program(self):
      self.eat(Token.PROGRAM)
      variable = self.variable()
      self.eat(Token.SEMI)
      block = self.block()
      self.eat(Token.DOT)
      self.eat(Token.EOF)
      return Program(name=variable.name, block=block)

   def parse(self):
      return self.program()

class Interpreter:
   TYPE_ASSOCIATION = {
      Token.INTEGER: int,
      Token.REAL: float,
   }

   def __init__(self, parser):
      self.parser = parser
      self.GLOBAL_SCOPE = {}

   def visit_binop(self, node):
      if node.op.type == Token.PLUS:
         return self.visit(node.left) + self.visit(node.right)
      if node.op.type == Token.MINUS:
         return self.visit(node.left) - self.visit(node.right)
      if node.op.type == Token.MUL:
         return self.visit(node.left) * self.visit(node.right)
      if node.op.type == Token.INTEGER_DIV:
         return self.visit(node.left) // self.visit(node.right)
      if node.op.type == Token.FLOAT_DIV:
         return self.visit(node.left) / self.visit(node.right)

   def visit_number(self, node):
      return node.value

   def visit_unaryop(self, node):
      op = node.op.type
      if op == Token.PLUS:
         return +self.visit(node.expr)
      elif op == Token.MINUS:
         return -self.visit(node.expr)

   def visit_assignop(self, node):
      var = self.GLOBAL_SCOPE.get(node.left.name, None)
      if not var:
         raise Exception('undefined variable {node.left.name}')
      
      value = self.visit(node.right)
      if not isinstance(value, Interpreter.TYPE_ASSOCIATION[var['type']]):
         raise Exception(f'misstyped assignment to variable {node.left.name}, expected an {var["type"]}')

      self.GLOBAL_SCOPE[node.left.name]['value'] = value

   def visit_var(self, node):
      name = node.name
      value = self.GLOBAL_SCOPE.get(name, None)['value']
      return value

   def visit_compound(self, node):
      for child in node.childrens:
         if isinstance(child, AssignOp):
            self.visit_assignop(child)
         if isinstance(child, Compound):
            self.visit_compound(child)

   def visit_type(self, node):
      return node.value

   def visit_block(self, node):
      for declaration in node.declarations:
         self.visit_vardecl(declaration)
      
      self.visit(node.compound)

   def visit_vardecl(self, node):
      self.GLOBAL_SCOPE[node.var_node.name] = {'value': None, 'type': self.visit_type(node.type_node)}

   def visit_program(self, node):
      self.visit_block(node.block_node)

   def visit(self, node):
      if isinstance(node, BinOp):
         return self.visit_binop(node)
      if isinstance(node, Number):
         return self.visit_number(node)
      if isinstance(node, UnaryOp):
         return self.visit_unaryop(node)
      if isinstance(node, Compound):
         return self.visit_compound(node)
      if isinstance(node, Var):
         return self.visit_var(node)
      if isinstance(node, AssignOp):
         return self.visit_assignop(node)
      if isinstance(node, Type):
         return self.visit_type(node)
      if isinstance(node, Program):
         return self.visit_program(node)
      if isinstance(node, Block):
         return self.visit_block(node)
      if isinstance(node, VarDecl):
         return self.visit_vardecl(node)
      raise Exception('unknown AST node type')

   def interpret(self):
      tree = self.parser.parse()
      self.visit(tree)
      return self.GLOBAL_SCOPE