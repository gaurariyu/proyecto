class Nodo:
    def __init__(self, valor, hijos=None):
        self.valor = valor
        self.hijos = hijos if hijos else []

    def __repr__(self):
        return f"Nodo({self.valor}, hijos={len(self.hijos)})"

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos] if self.tokens else None

    def eat(self, token_type, token_value=None):
        if self.current_token.type == token_type and (token_value is None or self.current_token.value == token_value):
            self.pos += 1
            if self.pos < len(self.tokens):
                self.current_token = self.tokens[self.pos]
            else:
                self.current_token = None
        else:
            expected_value = token_value if token_value else token_type
            raise Exception(f"Error sintáctico: se esperaba {expected_value} pero se encontró {self.current_token.type}")

    def factor(self):
        token = self.current_token
        if token.type == 'IDENTIFICADOR':
            self.eat('IDENTIFICADOR')
            return Nodo(token.value)
        elif token.type == 'LITERAL_NUMERICO':
            self.eat('LITERAL_NUMERICO')
            return Nodo(token.value)
        elif token.type == 'DELIMITADOR' and token.value == '(':
            self.eat('DELIMITADOR', '(')  # Consume '('
            expr_value = self.expression()  # Evaluamos lo que hay dentro de los paréntesis
            if self.current_token and self.current_token.value == ')':
                self.eat('DELIMITADOR', ')')  # Consume ')'
            else:
                raise Exception(f"Error sintáctico: falta ')' para cerrar el paréntesis.")
            return expr_value
        else:
            raise Exception(f"Error sintáctico en factor: {token}")

    def term(self):
        result = self.factor()
        while self.current_token and self.current_token.type == 'OPERADOR_ARITMETICO' and self.current_token.value in '*/%':
            operator = self.current_token
            self.eat('OPERADOR_ARITMETICO')
            right = self.factor()
            result = Nodo(operator.value, [result, right])
        return result

    def expression(self):
        # Primero evaluamos términos con multiplicación y división
        result = self.term()

        # Luego procesamos operadores aritméticos (suma/resta)
        while self.current_token and self.current_token.type == 'OPERADOR_ARITMETICO' and self.current_token.value in '+-':
            operator = self.current_token
            self.eat('OPERADOR_ARITMETICO')
            right = self.term()
            result = Nodo(operator.value, [result, right])

        # Soporte para operadores relacionales
        if self.current_token and self.current_token.type == 'OPERADOR_RELACIONAL':
            operator = self.current_token
            self.eat('OPERADOR_RELACIONAL')
            right = self.expression()  # Volvemos a evaluar la expresión después del operador relacional
            result = Nodo(operator.value, [result, right])

        return result

    def if_statement(self):
        self.eat('PALABRA_CLAVE', 'if')  # Consume 'if'

        # Verifica apertura de paréntesis (
        if self.current_token.value == '(':
            self.eat('DELIMITADOR', '(')
        else:
            raise Exception(f"Error sintáctico: se esperaba '(' pero se encontró {self.current_token.value}")

        condition = self.expression()  # Analiza la condición

        # Verifica cierre de paréntesis )
        if self.current_token and self.current_token.value == ')':
            self.eat('DELIMITADOR', ')')
        else:
            raise Exception(f"Error sintáctico: falta ')' para cerrar el paréntesis.")

        # Verifica apertura de llaves {
        if self.current_token and self.current_token.value == '{':
            self.eat('DELIMITADOR', '{')
        else:
            raise Exception(f"Error sintáctico: se esperaba '{{' pero se encontró {self.current_token.value}")

        # Procesa las sentencias dentro del bloque
        statements = []
        while self.current_token and self.current_token.value != '}':
            statements.append(self.statement())

        # Verifica el cierre de llaves }
        if self.current_token and self.current_token.value == '}':
            self.eat('DELIMITADOR', '}')
        else:
            raise Exception(f"Error sintáctico: falta '}}' para cerrar el bloque if.")

        return Nodo('IF', [condition, Nodo('BLOCK', statements)])

    def statement(self):
        if self.current_token.type == 'PALABRA_CLAVE' and self.current_token.value == 'if':
            return self.if_statement()
        elif self.current_token.type == 'IDENTIFICADOR':
            left = self.current_token
            self.eat('IDENTIFICADOR')
            if self.current_token.type == 'OPERADOR_ASIGNACION':
                operator = self.current_token
                self.eat('OPERADOR_ASIGNACION')
                right = self.expression()

                # Verificamos si el punto y coma está presente
                if self.current_token and self.current_token.type == 'DELIMITADOR' and self.current_token.value == ';':
                    self.eat('DELIMITADOR', ';')
                else:
                    raise Exception(f"Error sintáctico: falta ';' al final de la sentencia de asignación.")

                return Nodo('ASSIGN', [Nodo(left.value), Nodo(operator.value), right])
            else:
                raise Exception(f"Error sintáctico: se esperaba OPERADOR_ASIGNACION, pero se encontró {self.current_token.type}")
        else:
            raise Exception(f"Error sintáctico: sentencia desconocida iniciada por {self.current_token.type}")

    def parse(self):
        if self.current_token.type == 'PALABRA_CLAVE' and self.current_token.value == 'if':
            return self.if_statement()
        else:
            return self.statement()
