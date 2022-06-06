from lexer import Token
from parser import Integer, Boolean, ExprOp, CalcOp, BoolOp

# equivalent to xor
def inverse(bool, val):
   return (bool and not val) or (val and not bool)


class Interpreter:
   def __init__(self, parser):
      self.parser = parser
   
   def visit_integer(self, node):
      return node.value

   def visit_boolean(self, node):
      if node.bool:
         bool = True if node.bool.type == Token.TRUE else False
      else:
         val = self.visit(node.node)
         bool = False if val == 0 else True
      return inverse(node.inverse, bool)

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
         return inverse(node.inverse, (a and b))
      
      if node.op.type == Token.OR:
         return inverse(node.inverse, (a or b))

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