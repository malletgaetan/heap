from arithmetic_ast_lib import Token, Lexer, Parser, ASTNum, ASTOp

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