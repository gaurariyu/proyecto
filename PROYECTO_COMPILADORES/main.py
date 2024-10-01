from lexer import Lexer
from parser import Parser

def main():
    print("Ingresa el código fuente para analizar. Presiona Enter dos veces para comenzar:")
    print("EJEMPLO: if (x == 5) {y = 3 * x + 2;}")
    texto = ""
    while True:
        line = input()
        if line == "":
            break
        texto += line + "\n"

    lexer = Lexer(texto)
    tokens, errores = lexer.lex()

    if errores:
        print("\nErrores léxicos encontrados:")
        for error in errores:
            print(error)
    else:
        print("\nTokens reconocidos:")
        for token in tokens:
            print(token)

        parser = Parser(tokens)
        try:
            resultado = parser.parse()
            print("\nÁrbol sintáctico:", resultado)
        except Exception as e:
            print(f"\nError sintáctico: {e}")

if __name__ == '__main__':
    main()
