import re
from collections import defaultdict
from token import Token

tokens = [
    ('PALABRA_CLAVE', r'\b(if|else|while|for|return|true|false|null|None|float)\b'), 
    ('IDENTIFICADOR', r'[a-zA-Z_][a-zA-Z0-9_]*'), 
    ('LITERAL_NUMERICO', r'\b\d+(\.\d+)?\b'), 
    ('LITERAL_CADENA', r'\"(\\\\.|[^\"\\\\])*\"|\'(\\\\.|[^\'\\\\])*\''), 
    ('OPERADOR_ARITMETICO', r'[\+\-\*/%]'), 
    ('OPERADOR_RELACIONAL', r'(==|!=|<=|>=|<|>)'), 
    ('OPERADOR_LOGICO', r'&&|\|\||!'), 
    ('OPERADOR_ASIGNACION', r'=|\+=|-=|\*=|/='), 
    ('DELIMITADOR', r'[(){}\[\],;]'), 
    ('COMENTARIO_UNA_LINEA', r'//.*'), 
    ('COMENTARIO_MULTILINEA', r'/\*.*?\*/'), 
    ('COMENTARIO_UNA_LINEA_HASH', r'#.*'),  
    ('ESPACIO', r'\s+'), 
]

class Lexer:
    def __init__(self, texto):
        self.texto = texto

    def lex(self):
        pos = 0
        resultado = []
        errores = []
        while pos < len(self.texto):
            match = None
            for tipo, patron in tokens:
                regex = re.compile(patron)
                match = regex.match(self.texto, pos)
                if match:
                    valor = match.group(0)
                    if tipo not in ['COMENTARIO_UNA_LINEA', 'COMENTARIO_MULTILINEA', 'ESPACIO']:
                        resultado.append(Token(tipo, valor))
                    pos = match.end(0)
                    break
            if not match:
                errores.append(f"Caracter no válido: '{self.texto[pos]}' en posición {pos}")
                pos += 1
        return resultado, errores
