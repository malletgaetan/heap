from lexer import Lexer
from parser import Parser
from interpreter import Interpreter


def main():
   while True:
      try:
         text = input('eval>')
         lexer = Lexer(input=text)
         parser = Parser(lexer=lexer)
         interpreter = Interpreter(parser=parser)
         print(interpreter.interpret())
      except EOFError:
         continue
      except Exception as e:
         print(e)

if __name__ == '__main__':
   main()