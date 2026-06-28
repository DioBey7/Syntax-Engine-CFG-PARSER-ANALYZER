# ⚙️ Syntax Engine

**An Advanced BNF Syntax Analyzer with Recursive Backtracking, Static DFS Guard, Semantic Interpretation, and Visual Topology Generation.**

Syntax Engine is a high-performance, library-free syntax analysis framework designed to process dynamic Backus-Naur Form (BNF) grammars with integrated semantic interpretation capabilities. Built entirely from foundational principles, it features a custom recursive descent parser, automated left-recursion detection, an AST-based interpreter, and graphical parse tree visualization.

---

## 🚀 Core Features

- **Zero-Dependency Parsing:** A custom top-down Recursive Descent kernel built without external parser generator libraries (like NLTK or Lark).
- **Static Left-Recursion Guard:** Implements a pre-execution Depth-First Search (DFS) graph traversal algorithm to detect cyclic dependencies (e.g., *A → B → A*) and prevent infinite loops/stack overflow.
- **Intelligent Backtracking:** Accurate memory state management and token index restoration during failed non-deterministic derivation branches.
- **Semantic Interpretation Engine:** Built-in AST (Abstract Syntax Tree) evaluator for executing domain-specific commands such as NPC spawning and attribute assignment in game grammar contexts.
- **Dual Lexical Analysis Modes:** Flexible tokenization supporting both character-level and word-level lexical analysis with comprehensive error reporting.
- **Visual Topology Integration:** Automated generation of high-resolution parse tree topologies (PDF/PNG) using the Graphviz rendering engine.
- **Semantic Anomaly Diagnostics:** Goes beyond standard "Syntax Error" exceptions by providing highly contextual **WHERE, WHAT, and WHY** reports for derivation failures.
- **Clean JSON Serialization:** Actively strips linguistic formatting tags (`< >`) to produce pristine, dictionary-based JSON derivation structures.
- **Dual Interfaces:** Offers both a batch-testing Command Line Interface (`main_display.py`) and a feature-rich multi-threaded Graphical User Interface (`main_GUI.py`) with real-time execution feedback.

---

## 🏗️ Architecture Overview

### Core Components

#### 1. **Lexer** (`lexer.py`)
Tokenizes input source code into a structured token stream.

**Features:**
- Token classification (NUMBER, STRING, IDENTIFIER, OPERATOR, PUNCTUATION, COMMENT, KEYWORD)
- Line and column tracking for precise error diagnostics
- Support for multi-line input with proper newline handling
- Automatic comment and whitespace filtering

**Token Structure:**
```python
Token(type: str, value: str, line: int, column: int)
```

#### 2. **Parser** (`my_parser.py`)
Implements a top-down recursive descent parser with backtracking capabilities.

**Key Methods:**
- `parsing_rules(symbol)` - Performs recursive descent parsing for a given non-terminal symbol
- `detect_left_recursion()` - Executes DFS-based cycle detection to prevent infinite recursion
- `error_check(start_symbol)` - Generates contextual error diagnostics

**Algorithm Details:**
- Maintains parse state: current token index, maximum index reached, expected symbols at failure point
- Attempts production rules in order of decreasing length (longest-match-first strategy)
- Restores parser state on failed branches (intelligent backtracking)

#### 3. **Reader** (`my_reader.py`)
Parses grammar files and sentence input with robust error handling.

**Input Format:**
- **Grammar File:** BNF format with `::=` rule separator and `|` for alternatives
- **Sentences File:** Line-separated inputs, supporting both space-delimited tokens and epsilon (ε) symbol

#### 4. **Interpreter** (`interpreter.py`)
Evaluates parse trees to execute semantic actions and domain-specific operations.

**Supported Operations:**
- **Spawn Action:** `spawn <npc> at <zone>` → Creates NPC instance at specified zone
- **State Action:** `set <attribute> = <value>` → Assigns values to NPC attributes with memory persistence

**Output:** Structured system messages and memory-based state tracking

#### 5. **Parse Tree Generator** (`parse_tree_generator.py`)
Converts parse trees into both textual and graphical representations.

**Output Formats:**
- Plain-text indented tree structure
- PDF/PNG graphical topologies via Graphviz
- Entry-numbered outputs for batch processing

---

## 🛠️ System Requirements

### Software Requirements
- **Python:** 3.8 or higher
- **System Software:** [Graphviz Executable](https://gitlab.com/api/v4/projects/4207231/packages/generic/graphviz-releases/14.1.5/windows_10_cmake_Release_graphviz-install-14.1.5-win32.exe)
  - ⚠️ **CRITICAL:** During Graphviz installation, you **MUST** select *"Add Graphviz to the system PATH for all users"*

### Python Dependencies

Install required packages using pip:
```bash
pip install customtkinter graphviz Pillow
```

**Package Descriptions:**
- `customtkinter` - Modern dark-themed GUI framework
- `graphviz` - Python bindings for Graphviz rendering engine
- `Pillow` - Image processing and display

---

## 📦 Installation & Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/DioBey7/Syntax-Engine-CFG-PARSER-ANALYZER.git
cd Syntax-Engine-CFG-PARSER-ANALYZER
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

(Or manually: `pip install customtkinter graphviz Pillow`)

### Step 3: Install Graphviz System Software
Download and install from the link above, ensuring PATH configuration is enabled.

### Step 4: Verify Installation
```python
import graphviz
print(graphviz.version())  # Should output Graphviz version without errors
```

---

## 💻 Execution Modes

### Mode 1: Graphical User Interface (GUI)

The primary recommended interface for interactive testing and visualization.

```bash
python main_GUI.py
```

**Features:**
- **Sidebar Controls:**
  - LOAD GRAMMAR - Select BNF grammar file
  - LOAD SENTENCES - Select sentence input file
  - EXECUTE ENGINE - Run full analysis pipeline
  - DEVELOPER REPOSITORY - Quick link to GitHub profile

- **Multi-Tab Output:**
  - **PARSE TREE** - Display parse trees with optional graphical topology view
  - **JSON STRUCTURE** - Validated derivation structures in JSON format
  - **ANOMALY LOGS** - Detailed error diagnostics for invalid inputs

- **Kernel Console:**
  - Real-time execution logs
  - Timestamp-prefixed messages
  - System status indicators

- **Interactive Features:**
  - Animated progress bar during analysis
  - Sound effects (success, error, recursion alerts)
  - Graphical tree topology toggle
  - Multi-threaded background processing

### Mode 2: Command Line Interface (CLI)

For batch processing and automated testing workflows.

```bash
python main_display.py
```

**Features:**
- Sequential sentence analysis
- Console-based tree visualization
- JSON output to terminal
- Graphical PDF/PNG generation with automatic viewing
- Summary statistics (valid/invalid counts)

---

## 📖 Usage Example

### Grammar File Format (`grammar_game.txt`)
```bnf
<command> ::= <spawn_action> | <state_action>
<spawn_action> ::= spawn <npc> at <zone>
<state_action> ::= set <attribute> = <value>

<npc> ::= hunter | golem | boss
<zone> ::= dungeon | arena | sanctuary
<attribute> ::= aggro | health | speed
<value> ::= 100 | 80 | 0
```

### Sentence File Format (`sentences_game.txt`)
```
spawn hunter at arena
set aggro = 100
spawn boss at dungeon
set health = 80
spawn golem at tavern
```

### Expected Output

**Valid Sentence:**
```
Input: spawn hunter at arena
Valid
Parse tree:
<command>
├── <spawn_action>
│   ├── spawn
│   ├── <npc> → hunter
│   ├── at
│   └── <zone> → arena

AST ENGINE OUTPUT: SYSTEM: [HUNTER] named entity loaded at the [ARENA] region.

JSON:
{
  "command": {
    "spawn_action": {
      "npc": "hunter",
      "zone": "arena"
    }
  }
}
```

**Invalid Sentence:**
```
Input: spawn at hunter arena
Invalid
Error Diagnostics:
• WHERE: Satır 1, Sütun 2 (at token 'at')
• WHAT: "hunter", "golem", or "boss" was expected.
• WHY: after 'spawn', the grammar requires a valid NPC identifier to continue, but found 'at'
```

---

## 🔍 Advanced Features

### Left-Recursion Detection

The engine automatically detects and prevents left-recursive grammars before parsing begins:

```python
recursive_cycles = parser.detect_left_recursion()
if recursive_cycles:
    print("FATAL ERROR: Left Recursion detected")
    # E.g., A → B → A or A → A x
```

### Error Diagnostics System

Comprehensive error reporting with three contextual layers:

1. **WHERE:** Exact token position (line, column)
2. **WHAT:** Expected terminal/non-terminal symbols
3. **WHY:** Explanation of derivation failure in natural language

### Semantic Interpretation

The built-in interpreter executes domain-specific actions extracted from parse trees:

```python
engine = interpreter.Interpreter()
result = engine.evaluate(parse_tree)
# Executes spawn/set commands and maintains NPC state
```

### Graphical Parse Trees

Automated visual generation with Graphviz:

```bash
# Generated as: gui_1.pdf, gui_2.pdf, etc.
# Viewable in the GUI's PARSE TREE tab with topology toggle
```

---

## 📊 File Structure

```
Syntax-Engine-CFG-PARSER-ANALYZER/
├── lexer.py                          # Tokenization engine
├── my_parser.py                      # Recursive descent parser
├── my_reader.py                      # Grammar and sentence file reader
├── interpreter.py                    # AST evaluator
├── parse_tree_generator.py           # Tree visualization (text & graphical)
├── main_display.py                   # CLI execution interface
├── main_GUI.py                       # GUI execution interface
├── grammar_game.txt                  # Example game grammar (BNF)
├── sentences_game.txt                # Example game sentences
├── execution_and_dependency_notes.txt # Installation guide
├── README.md                         # This file
└── requirements.txt                  # Python dependencies
```

---

## 🧪 Testing & Validation

### Running Test Suites

The CLI mode provides automated batch testing:

```bash
python main_display.py
```

Configured to test against:
- `grammar1.txt` with `sentences.txt`
- `grammar2.txt` with `sentences2.txt`
- `grammar3.txt` with `sentences3.txt`

### Creating Custom Test Cases

1. **Define Grammar:**
   Create `my_grammar.txt` with BNF rules

2. **Create Sentence File:**
   Create `my_sentences.txt` with test inputs

3. **Run Parser:**
   - GUI: Load both files and click EXECUTE ENGINE
   - CLI: Modify `main_display.py` to reference your files

---

## 🔧 Troubleshooting

### Issue: "graphviz.ExecutableNotFound"
**Solution:** Graphviz is not installed or not in PATH
- Re-run Graphviz installer
- Ensure *"Add Graphviz to the system PATH"* is checked
- Restart Python/IDE after installation

### Issue: GUI doesn't display graphical trees
**Solution:** Graphviz rendering failure
- Check `PARSE TREE` → `ANOMALY LOGS` tab for error details
- Verify Graphviz installation with: `dot -V`

### Issue: Parser hangs or crashes
**Solution:** Left recursion detected
- Check grammar for circular dependencies
- Run `detect_left_recursion()` in isolation
- Refactor grammar to eliminate cycles

### Issue: Incorrect parsing results
**Solution:** Check grammar or tokenization
- Verify BNF syntax (use `::=` and `|` correctly)
- Review lexer token specifications in `lexer.py`
- Add test sentences one-by-one for isolation

---

## 🎨 GUI Customization

### Theme Settings
Located in `main_GUI.py`:
```python
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")
```

Options: `"Dark"`, `"Light"`, `"System"` for mode  
Colors: `"blue"`, `"green"`, `"red"`, `"purple"`, etc.

### Sound Effects
Control in `play_sound()` method:
```python
if sound_type == "success":
    for freq in [600, 800, 1200]:
        winsound.Beep(freq, 150)
```

---

## 📚 Language Composition

- **Python:** 65% (Core engine and interfaces)
- **TeX/Documentation:** 35% (Mathematical notation and formal specifications)

---

## 📝 License

This project is provided as-is for educational and research purposes.

---

## 👨‍💻 Author

**DioBey7**  
GitHub: [@DioBey7](https://github.com/DioBey7)

---

## 🤝 Contributing

Contributions, bug reports, and feature requests are welcome. Feel free to:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit changes (`git commit -m 'Add YourFeature'`)
4. Push to branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

---

## 📞 Support

For issues, questions, or feature requests:
- Open an issue on [GitHub Issues](https://github.com/DioBey7/Syntax-Engine-CFG-PARSER-ANALYZER/issues)
- Check existing documentation in `execution_and_dependency_notes.txt`

---

## 🎯 Future Roadmap

- [ ] LL(1) grammar analysis and conversion
- [ ] SLR parser implementation as alternative to recursive descent
- [ ] Extended interpreter with variable scoping and functions
- [ ] Interactive grammar debugging mode
- [ ] Export parse trees in AST JSON format
- [ ] Multi-language semantic action definitions

---

**Version:** Academic Build
**Last Updated:** June 2026  
**Status:** Active Development
