import os

class Reader:
    def __init__(self, grammar_file, sentences_file):
        self.grammar_path = os.path.join(os.path.dirname(__file__), grammar_file)
        self.sentences_path = os.path.join(os.path.dirname(__file__), sentences_file)

    def read_bnf_grammar(self): 
        grammar = {}
        last_lhs = None
        try:
            with open(self.grammar_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line: continue
                    if "::=" in line:
                        lhs, rhs = line.split("::=")
                        lhs = lhs.strip()
                        last_lhs = lhs
                        alternatives = [alt.strip().split() for alt in rhs.split("|") if alt.strip()]
                        alternatives.sort(key=len, reverse=True)
                        grammar[lhs] = alternatives
                    elif last_lhs:
                        extra_alts = [alt.strip().split() for alt in line.split("|") if alt.strip()]
                        grammar[last_lhs].extend(extra_alts)
            return grammar
        except FileNotFoundError: return {}

    def read_sentences(self): 
        sentences = []
        try:
            with open(self.sentences_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line: continue
                    if " " not in line and line != "ε":
                        sentences.append(list(line))
                    else:
                        sentences.append(line.split())
            return sentences
        except FileNotFoundError: return []