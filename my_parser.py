import my_reader
import lexer

class Parser:
    def __init__(self, grammar_file, sentences_file):
        self.reader = my_reader.Reader(grammar_file, sentences_file)
        self.grammar = self.reader.read_bnf_grammar()
        self.sentences = self.reader.read_sentences()
        self.lexer = lexer.Lexer()
        self.current_index = 0
        self.tokens = []
        self.max_idx = 0
        self.expected_at_max = []

    def detect_left_recursion(self):
        dependencies = {}
        for lhs, productions in self.grammar.items():
            first_symbols = set()
            for prod in productions:
                if prod and prod[0] in self.grammar:
                    first_symbols.add(prod[0])
            dependencies[lhs] = first_symbols

        cycles = []
        visited = {}
        path = []

        def dfs(node):
            if node in path:
                start = path.index(node)
                cycles.append(path[start:] + [node])
                return
            if visited.get(node): return
            path.append(node)
            for neighbor in dependencies.get(node, []):
                dfs(neighbor)
            path.pop()
            visited[node] = True

        for nt in self.grammar:
            dfs(nt)
        return cycles

    def parsing_rules(self, symbol):
        if symbol == "ε":
            return "ε"

        if symbol not in self.grammar:
            if self.current_index < len(self.tokens):
                current_token = self.tokens[self.current_index]
                if current_token.value == symbol:
                    self.current_index += 1
                    return current_token.value
            
            if self.current_index >= self.max_idx:
                if self.current_index > self.max_idx:
                    self.max_idx = self.current_index
                    self.expected_at_max = []
                if symbol not in self.expected_at_max:
                    self.expected_at_max.append(symbol)
            return None

        start_pos = self.current_index
        sorted_productions = sorted(self.grammar[symbol], key=len, reverse=True)

        for production in sorted_productions:
            self.current_index = start_pos
            children = {}
            match_all = True

            for part in production:
                res = self.parsing_rules(part)
                if res is not None:
                    children[part] = res
                else:
                    match_all = False
                    break

            if match_all:
                return children
        return None

    def error_check(self, start_symbol):
        if self.max_idx < len(self.tokens):
            err_token = self.tokens[self.max_idx]
            token_label = err_token.value
            location_info = f"Satır {err_token.line}, Sütun {err_token.column}"
        else:
            token_label = "EOF"
            location_info = "Belge Sonu"

        expected_str = ' or '.join([f'"{e}"' for e in self.expected_at_max])
        why_msg = ""
        
        if self.max_idx == 0:
            why_msg = f"the sentence begins with '{token_label}', but grammar requires {expected_str} to start"
        else:
            prev_token = self.tokens[self.max_idx - 1].value
            why_msg = f"after '{prev_token}', the grammar requires {expected_str} to continue the sequence, but found '{token_label}'"

        print("Invalid\n")
        print("Error Diagnostics:")
        print(f"• WHERE : {location_info} (at token '{token_label}')")
        print(f"• WHAT  : {expected_str} was expected.")
        print(f"• WHY   : {why_msg}")