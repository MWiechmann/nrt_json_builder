import json
import copy
import os 
import tkinter as tk
import pymsgbox as pmb
from tkinter import font
from tkinter import filedialog

# set base settings (use default for now)
base_set = { 
  "prompt_filename": "prompt.txt",
  "output_prefix": "k1_tests/out",
  "iterations": 1,
  "generations": 20,
  "parameters": {
    "model": "6B-v3",
    "prefix": "vanilla",
    "temperature": 0.55,
    "max_length": 40,
    "min_length": 40,
    "top_k": 140,
    "top_p": 0.9,
    "tail_free_sampling": 1,
    "repetition_penalty": 3.5,
    "repetition_penalty_range": 1024,
    "repetition_penalty_slope": 6.57,
    "bad_words_ids": [],
    "ban_brackets": True,
    "use_cache": False,
    "use_string": False,
    "return_full_text": False
    }
}

# Define tk Class for entering parameters:
class CustomBase(tk.Frame):
    def __init__(self,master=None,**kw):
        self.params = {}
        tk.Frame.__init__(self,master=master,**kw)

        default_font = tk.font.nametofont("TkDefaultFont")
        default_font.configure(family="Arial", size=12)

        tk.Label(self,text="Model").grid(row=0,column=0, sticky="E")
        self.model = tk.Entry(self, font=('Arial', 12))
        self.model.grid(row=0,column=1)
        self.model.insert(0, "6B-v3")

        tk.Label(self,text="prefix").grid(row=1,column=0, sticky="E")
        self.prefix = tk.Entry(self, font=('Arial', 12))
        self.prefix.grid(row=1,column=1)
        self.prefix.insert(0, "vanilla")

        tk.Label(self,text="temperature (randomness)").grid(row=2,column=0, sticky="E")
        self.temp = tk.Entry(self, font=('Arial', 12))
        self.temp.grid(row=2,column=1)
        self.temp.insert(0, "0.55")

        tk.Label(self,text="max length").grid(row=3,column=0, sticky="E")
        self.max_len = tk.Entry(self, font=('Arial', 12))
        self.max_len.grid(row=3,column=1)
        self.max_len.insert(0, "40")

        tk.Label(self,text="min length").grid(row=4,column=0, sticky="E")
        self.min_len = tk.Entry(self, font=('Arial', 12))
        self.min_len.grid(row=4,column=1)
        self.min_len.insert(0, "40")

        tk.Label(self,text="Top-k").grid(row=5,column=0, sticky="E")
        self.top_k = tk.Entry(self, font=('Arial', 12))
        self.top_k.grid(row=5,column=1)
        self.top_k.insert(0, "140")

        tk.Label(self,text="Top-p").grid(row=6,column=0, sticky="E")
        self.top_p = tk.Entry(self, font=('Arial', 12))
        self.top_p.grid(row=6,column=1)
        self.top_p.insert(0, "0.9")

        tk.Label(self,text="Tail-Free-Sampling (1 = disabled)").grid(row=7,column=0, sticky="E")
        self.tfs = tk.Entry(self, font=('Arial', 12))
        self.tfs.grid(row=7,column=1)
        self.tfs.insert(0, "1")

        tk.Label(self,text="Repetition Penalty").grid(row=8,column=0, sticky="E")
        self.rep_pen = tk.Entry(self, font=('Arial', 12))
        self.rep_pen.grid(row=8,column=1)
        self.rep_pen.insert(0, "3.5")

        tk.Label(self,text="Repetition Penalty Range").grid(row=9,column=0, sticky="E")
        self.rep_pen_range = tk.Entry(self, font=('Arial', 12))
        self.rep_pen_range.grid(row=9,column=1)
        self.rep_pen_range.insert(0, "1024")

        tk.Label(self,text="Repetition Penalty Slope").grid(row=10,column=0, sticky="E")
        self.rep_pen_slope = tk.Entry(self, font=('Arial', 12))
        self.rep_pen_slope.grid(row=10,column=1)
        self.rep_pen_slope.insert(0, "6.57")

        tk.Button(self,text="Go",command = self.collectparams).grid(row=11,column=1)


    def collectparams(self):
        self.params['model'] = self.model.get()
        self.params['prefix'] = self.prefix.get()
        self.params['temperature'] = self.temp.get()
        self.params['max_length'] = self.max_len.get()
        self.params['min_length'] = self.min_len.get()
        self.params['top_k'] = self.top_k.get()
        self.params['top_p'] = self.top_p.get()
        self.params['tail_free_sampling'] = self.tfs.get()
        self.params['repetition_penalty'] = self.rep_pen.get()
        self.params['repetition_penalty_range'] = self.rep_pen_range.get()
        self.params['repetition_penalty_slope'] = self.rep_pen_slope.get()
        adjust_base_params(self.params)

def adjust_base_params(params):
    for key in base_set["parameters"]:
    	if key in params:
    		base_set[key] = params[key]

# Prompt user to choose base params
base_choice = pmb.confirm("Please select your base setting", "Base Setting", ["Default", "Top-k = 1", "Custom"])

# adjust base settings according to choice
if base_choice == "Top-k = 1":
	base_set["parameters"]["top_k"] = 1
elif base_choice == "Custom":
	if __name__ == '__main__':
		root = tk.Tk()
		root.title("Set Base Parameters")
		CustomBase(root).grid()
		root.mainloop()

# Prompt user about True/False choices

brackets_choice = pmb.confirm("Do you want to ban brackets? (default = Yes)", "Ban Brackets", ["Yes", "No"])
if brackets_choice == "Yes":
	base_set["parameters"]["ban_brackets"] = True
else:
	base_set["parameters"]["ban_brackets"] = False

# select base prompt
current_dir = os.path.dirname(os.path.realpath(__file__))
base_prompt = tk.filedialog.askopenfilename(initialdir = current_dir, title = "Choose base prompt",
	filetypes = (("txt files","*.txt"),("all files","*.*")))
base_prompt_rel = os.path.relpath(base_prompt)
base_set["prompt_filename"] = base_prompt_rel

# select output folder
output_folder = tk.filedialog.askdirectory(initialdir = current_dir, title = "Choose output folder")
output_folder_rel = os.path.relpath(output_folder)

# choose output prefix
output_pre = pmb.prompt("Enter the prefix for your output", default="out")
output_folder_prefix = output_folder_rel + "/" output_pre
base_set["output_prefix"] = output_folder_prefix