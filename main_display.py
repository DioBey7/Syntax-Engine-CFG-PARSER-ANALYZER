# I have created a main display script to run the parser and visualize results in the terminal and as graphical parse trees. 
# It also checks for left recursion in the grammar and handles errors gracefully.

import my_parser as mp
import parse_tree_generator as tree_gen
import json

def clean_json(data):
    if isinstance(data, dict):
        return {k.replace("<", "").replace(">", ""): clean_json(v) for k, v in data.items()}
    return data

def run_test(grammar_file, sentences_file):
    print(f"\n{'_'*10} ANALYZING: {grammar_file} {'_'*10}\n")
    p = mp.Parser(grammar_file, sentences_file)
    
    recursive_cycles = p.detect_left_recursion()
    if recursive_cycles:
        print("FATAL ERROR: Left Recursion detected in grammar rules.\n")
        return

    start_symbol = list(p.grammar.keys())[0]
    valid_count = 0
    total_count = len(p.sentences)

    for i, s in enumerate(p.sentences):
        print("-" * 40)
        p.tokens = [t for t in s if t != "ε"]
        p.current_index = 0
        p.max_idx = 0
        p.expected_at_max = []
        
        print(f"Input: {' '.join(s)}")
        result = p.parsing_rules(start_symbol)
        
        if result is not None and p.current_index == len(p.tokens):
            valid_count += 1
            print("Valid") 
            print("Parse tree:\n")
            print(tree_gen.generate_parse_tree({start_symbol: result}))
            print("JSON:")
            print(json.dumps(clean_json({start_symbol: result}), indent=4, ensure_ascii=False))
            
            try:
                entry_name = f"{grammar_file.split('.')[0]}_entry_{i+1}"
                tree_gen.generate_graphical_tree({start_symbol: result}, entry_num=entry_name, output_format='pdf', view=True)
            except Exception:
                pass
        else:
            p.error_check(s, start_symbol)

    print(f"\n{grammar_file} Results: {valid_count}/{total_count} sentences are syntactically valid.")

if __name__ == "__main__":
    run_test("grammar1.txt", "sentences.txt")
    run_test("grammar2.txt", "sentences2.txt")
    run_test("grammar3.txt", "sentences3.txt") # My additional grammar and sentences for testing different scenarios