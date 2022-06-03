# 7+(2*(4+5+6*(4+5)*3)/2) => 7 2 4 5+ 6 4 5+* 3*+2/+
# https://en.wikipedia.org/wiki/Reverse_Polish_notation

# so we'll first create an AST from the calculus string, then translate the AST into reverse polish notation calculus


from arithmetic_ast_lib import Lexer, Parser, ASTOp

def polish_translate(node):
   calc = ""
   calc += polish_translate(node.left) if isinstance(node.left, ASTOp) else str(node.left.value)
   calc += polish_translate(node.right) if isinstance(node.right, ASTOp) else str(node.right.value)
   calc += node.operator.value
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
      print(polish_translate(ast))
	
if __name__ == "__main__":
	main()