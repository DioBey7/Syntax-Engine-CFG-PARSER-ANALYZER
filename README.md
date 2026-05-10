# ⚙️ Syntax Engine

**An Advanced BNF Syntax Analyzer with Recursive Backtracking, Static DFS Guard, and Visual Topology.**

Syntax Engine is a high-performance, library-free syntax analysis framework designed to process dynamic Backus-Naur Form (BNF) grammars. Built entirely from foundational principles, it features a custom Recursive Descent analyzer equipped with state-aware backtracking, automated Graphviz reporting, and contextual semantic error diagnostics.

## 🚀 Core Features

* **Zero-Dependency Parsing:** A custom top-down Recursive Descent kernel built without external parser generator libraries (like NLTK or Lark).
* **Static Left-Recursion Guard:** Implements a pre-execution Depth-First Search (DFS) graph traversal algorithm to detect cyclic dependencies (e.g., $A \to B \to A$) and prevent infinite loops/stack overflows.
* **Intelligent Backtracking:** Accurate memory state management and token index restoration during failed non-deterministic derivation branches.
* **Visual Topology Integration:** Automated generation of high-resolution parse tree topologies (PDF/PNG) using the Graphviz rendering engine.
* **Semantic Anomaly Diagnostics:** Goes beyond standard "Syntax Error" exceptions by providing highly contextual **Where, What, and Why** reports for derivation failures.
* **Clean JSON Serialization:** Actively strips linguistic formatting tags (`< >`) to produce pristine, dictionary-based JSON derivation structures.
* **Dual Interfaces:** Offers both a batch-testing Command Line Interface (`main_display.py`) and a multi-threaded Graphical User Interface (`main_GUI.py`).

## 🛠️ System Requirements

* **Python:** 3.8 or higher.
* **Python Packages:** `customtkinter`, `graphviz`, `Pillow`
* **System Software:** [Graphviz Executable](https://gitlab.com/api/v4/projects/4207231/packages/generic/graphviz-releases/14.1.5/windows_10_cmake_Release_graphviz-install-14.1.5-win32.exe) must be installed on your OS. 
    > ⚠️ **CRITICAL:** During the Graphviz installation, you MUST check the box that says *"Add Graphviz to the system PATH for all users"*.

## 💻 Execution

**To launch the Graphical User Interface (GUI):**
```bash
python main_GUI.py