from csv import list_dialects
from arithmetic_ast_lib import Lexer, Parser, ASTOp

def lisp_translator(node):
   calc = "("
   calc += node.operator.value
   calc += lisp_translator(node.left) if isinstance(node.left, ASTOp) else str(node.left.value)
   calc += lisp_translator(node.right) if isinstance(node.right, ASTOp) else str(node.right.value)
   calc += ")"
   return calc


def main():
   while True:
      try:
         text = input("calc> ")
      except EOFError:
         break
      if not text:
         continue
      lexer = Lexer(calculus=text)
      parser = Parser(lexer=lexer)
      ast= parser.parse()
      print(lisp_translator(ast))
	
if __name__ == "__main__":
	main()