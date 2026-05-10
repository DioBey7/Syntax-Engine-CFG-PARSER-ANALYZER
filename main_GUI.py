# Not necessary for the project but I wanted to add a little bit of polish to the user experience with the GUI and make it more engaging and fun to use.
# I also wanted to challenge myself to create a more complex and feature-rich interface, which is why I chose to use customtkinter and add elements like progress bars, sound effects, and a graphical tree view.
# Overall, I think it adds a nice touch to the project and makes it more enjoyable to interact with.

import customtkinter as ctk
import my_parser as mp
import parse_tree_generator as tree_gen
import json
import winsound
import threading
import time
import webbrowser 
from PIL import Image
from tkinter import filedialog
from datetime import datetime

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

def clean_json(data):
    if isinstance(data, dict):
        return {k.replace("<", "").replace(">", ""): clean_json(v) for k, v in data.items()}
    return data

class SyntaxEngine(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SYNTAX ENGINE | CFG PARSER & ANALYZER")
        self.geometry("1300x950")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color="#080808")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="SYNTAX ENGINE", 
                                      font=ctk.CTkFont(size=28, weight="bold", family="Orbitron"))
        self.logo_label.pack(padx=20, pady=(30, 0))
        
        self.version_label = ctk.CTkLabel(self.sidebar_frame, text="ACADEMIC BUILD 443728", font=ctk.CTkFont(size=10), text_color="#444444")
        self.version_label.pack(pady=(0, 20))

        self.btn_grammar = ctk.CTkButton(self.sidebar_frame, text="LOAD GRAMMAR", 
                                         fg_color="#121212", hover_color="#222222", command=self.load_grammar)
        self.btn_grammar.pack(padx=20, pady=10, fill="x")

        self.btn_sentences = ctk.CTkButton(self.sidebar_frame, text="LOAD SENTENCES", 
                                           fg_color="#121212", hover_color="#222222", command=self.load_sentences)
        self.btn_sentences.pack(padx=20, pady=10, fill="x")

        self.btn_github = ctk.CTkButton(self.sidebar_frame, text="DEVELOPER REPOSITORY", 
                                        fg_color="#0a0a0a", border_width=1, border_color="#1a1a1a",
                                        hover_color="#333333", text_color="#777777",
                                        font=ctk.CTkFont(size=11, family="Consolas"), command=self.advertise_yourself)
        self.btn_github.pack(padx=20, pady=10, fill="x")

        self.spacer = ctk.CTkLabel(self.sidebar_frame, text="")
        self.spacer.pack(expand=True)
        
        self.progress_bar = ctk.CTkProgressBar(self.sidebar_frame, orientation="horizontal", height=2, fg_color="#111111", progress_color="#2ecc71")
        self.progress_bar.set(0)
        self.progress_bar.pack(padx=20, pady=10, fill="x")

        self.btn_run = ctk.CTkButton(self.sidebar_frame, text="EXECUTE ENGINE", 
                                     fg_color="#1a1a1a", border_width=1, border_color="#2ecc71",
                                     hover_color="#2ecc71", text_color="#2ecc71",
                                     font=ctk.CTkFont(weight="bold"), command=self.run_engine)
        self.btn_run.pack(padx=20, pady=30, fill="x")

        self.main_container = ctk.CTkFrame(self, corner_radius=0, fg_color="#101010")
        self.main_container.grid(row=0, column=1, sticky="nsew")

        self.tabview = ctk.CTkTabview(self.main_container, fg_color="#0A0A0A", 
                                      segmented_button_selected_color="#2ecc71",
                                      segmented_button_unselected_color="#151515")
        self.tabview.pack(fill="both", expand=True, padx=20, pady=(20, 10))
        
        self.tab_tree = self.tabview.add(" PARSE TREE ")
        self.tab_json = self.tabview.add(" JSON STRUCTURE ")
        self.tab_errors = self.tabview.add(" ANOMALY LOGS ")

        self.tree_header = ctk.CTkFrame(self.tab_tree, fg_color="transparent", height=40)
        self.tree_header.pack(fill="x", padx=10, pady=5)
        
        self.view_mode_switch = ctk.CTkSwitch(self.tree_header, text="GRAPHICAL TOPOLOGY VIEW", command=self.toggle_tree_view, progress_color="#2ecc71")
        self.view_mode_switch.pack(side="right", padx=20)

        self.tree_content_frame = ctk.CTkFrame(self.tab_tree, fg_color="transparent")
        self.tree_content_frame.pack(fill="both", expand=True)

        self.tree_out = ctk.CTkTextbox(self.tree_content_frame, font=("Consolas", 15), fg_color="#050505", text_color="#BBBBBB")
        self.tree_out.pack(fill="both", expand=True)

        self.tree_image_view = ctk.CTkScrollableFrame(self.tree_content_frame, fg_color="#050505")

        self.json_out = ctk.CTkTextbox(self.tab_json, font=("Consolas", 15), fg_color="#050505", text_color="#2ecc71")
        self.json_out.pack(fill="both", expand=True)

        self.error_out = ctk.CTkTextbox(self.tab_errors, font=("Consolas", 14), fg_color="#050505", text_color="#E74C3C")
        self.error_out.pack(fill="both", expand=True)

        self.kernel_frame = ctk.CTkFrame(self.main_container, height=150, fg_color="#000000", border_width=1, border_color="#222222")
        self.kernel_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.kernel_log = ctk.CTkTextbox(self.kernel_frame, height=120, font=("Consolas", 12), 
                                         fg_color="#000000", text_color="#2ecc71", border_width=0)
        self.kernel_log.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.log_kernel("Core systems online. Ready for formal analysis.")

        self.grammar_file = None
        self.sentences_file = None
        self.image_labels = []

    def toggle_tree_view(self):
        self.play_sound("click")
        if self.view_mode_switch.get() == 1:
            self.tree_out.pack_forget()
            self.tree_image_view.pack(fill="both", expand=True)
        else:
            self.tree_image_view.pack_forget()
            self.tree_out.pack(fill="both", expand=True)

    def advertise_yourself(self):
        self.play_sound("click")
        webbrowser.open_new_tab("https://github.com/DioBey7?tab=repositories")
        self.log_kernel("Redirecting to Developer Repository...")

    def play_sound(self, sound_type):
        def _sound():
            if sound_type == "success":
                for freq in [600, 800, 1200]:
                    winsound.Beep(freq, 150)
            elif sound_type == "error":
                winsound.Beep(350, 500)
            elif sound_type == "click":
                winsound.Beep(1800, 50)
            elif sound_type == "recursion_alert":
                for _ in range(3):
                    winsound.Beep(1600, 100)
                    winsound.Beep(1200, 100)
        threading.Thread(target=_sound, daemon=True).start()

    def log_kernel(self, message, is_error=False):
        timestamp = datetime.now().strftime("%H:%M:%S")
        tag = "[!]" if is_error else "[+]"
        self.kernel_log.insert("end", f"[{timestamp}] {tag} {message}\n")
        self.kernel_log.see("end")

    def animate_progress(self, duration=0.8):
        def _animate():
            self.progress_bar.set(0)
            for i in range(21):
                self.progress_bar.set(i / 20)
                time.sleep(duration / 20)
        threading.Thread(target=_animate, daemon=True).start()

    def load_grammar(self):
        self.play_sound("click")
        path = filedialog.askopenfilename(title="Select BNF Grammar File")
        if path:
            self.grammar_file = path
            self.log_kernel(f"Grammar successfully mapped: {path.split('/')[-1]}")
            self.btn_grammar.configure(text_color="#2ecc71")

    def load_sentences(self):
        self.play_sound("click")
        path = filedialog.askopenfilename(title="Select Sentences File")
        if path:
            self.sentences_file = path
            self.log_kernel(f"Input stream target: {path.split('/')[-1]}")
            self.btn_sentences.configure(text_color="#2ecc71")

    def run_engine(self):
        if not self.grammar_file or not self.sentences_file:
            self.play_sound("error")
            self.log_kernel("HALTED: Input/Context parameters required.", True)
            return
        
        self.play_sound("click") 
        self.animate_progress()
        self.tree_out.delete("1.0", "end")
        self.json_out.delete("1.0", "end")
        self.error_out.delete("1.0", "end")

        for lbl in self.image_labels:
            lbl.destroy()
        self.image_labels = []
        
        self.log_kernel("Initiating formal analysis of input stream...")

        try:
            p = mp.Parser(self.grammar_file, self.sentences_file)
            
            recursive_cycles = p.detect_left_recursion()
            if recursive_cycles:
                self.play_sound("recursion_alert")
                self.log_kernel("ABORTED: Recursive instability detected.", True)
                self.error_out.insert("end", "SYNTAX ENGINE ERROR: STACK OVERFLOW PREVENTION\n" + "="*50 + "\n")
                self.tabview.set(" ANOMALY LOGS ")
                return

            start_symbol = list(p.grammar.keys())[0]
            valid_count = 0

            for i, s in enumerate(p.sentences):
                p.tokens = [t for t in s if t != "ε"]
                p.current_index = 0
                p.max_idx = 0
                p.expected_at_max = []
                
                result = p.parsing_rules(start_symbol)
                
                if result is not None and p.current_index == len(p.tokens):
                    valid_count += 1
                    
                    tree_str = tree_gen.generate_parse_tree({start_symbol: result})
                    self.tree_out.insert("end", f"Input: {' '.join(s)}\nValid\nParse tree:\n\n")
                    self.tree_out.insert("end", tree_str + "\n\n")
                    
                    self.json_out.insert("end", f"// VALIDATED ENTRY {i+1}\n")
                    self.json_out.insert("end", json.dumps(clean_json({start_symbol: result}), indent=4, ensure_ascii=False) + "\n\n")

                    try:
                        img_path = tree_gen.generate_graphical_tree({start_symbol: result}, entry_num=f"gui_{i+1}")
                        img = Image.open(img_path)
                        
                        w, h = img.size
                        max_w = 900
                        if w > max_w:
                            new_w = max_w
                            new_h = int(h * (max_w / w))
                        else:
                            new_w, new_h = w, h
                            
                        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(new_w, new_h))
                        
                        title_lbl = ctk.CTkLabel(self.tree_image_view, text=f"ENTRY #{i+1}", font=ctk.CTkFont(size=16, weight="bold"))
                        title_lbl.pack(pady=(20, 5))
                        
                        img_lbl = ctk.CTkLabel(self.tree_image_view, text="", image=ctk_img)
                        img_lbl.pack(pady=(0, 20), padx=10)
                        
                        self.image_labels.extend([title_lbl, img_lbl])
                        self.log_kernel(f"Graphical Topology generated for Entry {i+1}")
                        
                    except Exception as e:
                        self.log_kernel(f"Topology Error: {str(e)}", True)
                else:
                    self.tree_out.insert("end", f"Input: {' '.join(s)}\nInvalid\n\n")
                    
                    token_label = s[p.max_idx] if p.max_idx < len(s) else "EOF"
                    expected_str = ' or '.join([f'"{e}"' for e in p.expected_at_max])
                    
                    why_msg = ""
                    if p.max_idx == 0:
                        why_msg = f"the sentence begins with '{token_label}', but grammar requires {expected_str} to start"
                    else:
                        prev_token = s[p.max_idx - 1]
                        why_msg = f"after '{prev_token}', the grammar requires {expected_str} to continue the sequence, but found '{token_label}'"

                    self.error_out.insert("end", f"Input: {' '.join(s)}\nInvalid\nError:\n")
                    self.error_out.insert("end", f"•Where the error occurs: at token {p.max_idx + 1} (\"{token_label}\")\n")
                    self.error_out.insert("end", f"•What was expected: {expected_str}\n")
                    self.error_out.insert("end", f"•Why the sentence is invalid: {why_msg}\n\n{'-'*40}\n\n")

            if valid_count == len(p.sentences) and valid_count > 0:
                self.play_sound("success")
            elif valid_count == 0:
                self.play_sound("error")
            else:
                self.play_sound("click")

            self.log_kernel(f"Engine Cycle Complete. Results: {valid_count}/{len(p.sentences)} Validated.")

        except Exception as e:
            self.play_sound("error")
            self.log_kernel(f"FATAL KERNEL EXCEPTION: {str(e)}", True)

if __name__ == "__main__":
    app = SyntaxEngine()
    app.mainloop()