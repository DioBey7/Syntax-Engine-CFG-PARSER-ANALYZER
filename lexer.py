import re
from typing import NamedTuple, List

class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int

class Lexer:
    def __init__(self):
        self.token_specification = [
            ('NUMBER',    r'\d+(\.\d*)?'),  
            ('STRING',    r'"[^"]*"'),      
            ('IDENTIFIER',r'[A-Za-z_]\w*'), 
            ('OPERATOR',  r'[+\-*/=><!]+'), 
            ('PUNCT',     r'[(),;{}[\]]'),  
            ('COMMENT',   r'//.*'),         
            ('NEWLINE',   r'\n'),           
            ('SKIP',      r'[ \t]+'),       
            ('MISMATCH',  r'.'),            
        ]
        self.tok_regex = re.compile('|'.join('(?P<%s>%s)' % pair for pair in self.token_specification))

    def tokenize(self, code: str) -> List[Token]:
        tokens = []
        line_num = 1
        line_start = 0
        
        for mo in self.tok_regex.finditer(code):
            kind = mo.lastgroup
            value = mo.group()
            column = mo.start() - line_start
            
            if kind == 'NUMBER':
                value = float(value) if '.' in value else int(value)
            elif kind == 'STRING':
                value = value.strip('"') 
            elif kind == 'ID' and kind in ['if', 'then', 'else', 'while']:
                kind = 'KEYWORD' 
            elif kind == 'COMMENT' or kind == 'SKIP':
                continue 
            elif kind == 'NEWLINE':
                line_start = mo.end()
                line_num += 1
                continue
            elif kind == 'MISMATCH':
                raise RuntimeError(f'Lexical Error: Beklenmeyen karakter {value!r} satır {line_num}')
            
            tokens.append(Token(kind, str(value), line_num, column))
            
        return tokens

if __name__ == '__main__':
    lexer = Lexer()
    test_code = """
    // Bu bir test yorumudur
    the man saw a dog
    3 + 5 * (10 - 2)
    """
    
    tokens = lexer.tokenize(test_code)
    for tok in tokens:
        print(f"[{tok.type}] -> '{tok.value}' (Satır: {tok.line}, Sütun: {tok.column})")