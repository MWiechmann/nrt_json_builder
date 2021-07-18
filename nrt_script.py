import json
import copy
import os 
import tkinter as tk
import pymsgbox as pmb
from tkinter import font
from tkinter import filedialog

### BASE SETTINGS

# set base settings (use default for now)
base_set = { 
  "prompt_filename": "prompt.txt",
  "memory": "",
  "authors_note": "",
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
    },
    "permutations": [{}]
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
        self.master.destroy()

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
pmb.alert("Now you will choose the file that has the base prompt to use as input.", "Base Prompt")
current_dir = os.path.dirname(os.path.realpath(__file__))
base_prompt = tk.filedialog.askopenfilename(initialdir = current_dir, title = "Choose base prompt",
	filetypes = (("txt files","*.txt"),("all files","*.*")))
base_prompt_rel = os.path.relpath(base_prompt)
base_set["prompt_filename"] = base_prompt_rel

# Set memory & A/N
memory = pmb.prompt("Enter the memory for the input (or leave empty for no memory)", title= "Memory", default="")
authors_note = pmb.prompt("Enter the author's note for the input (or leave empty for no A/N)", title= "Author's Note",default="")
base_set["memory"] = memory
base_set["authors_note"] = authors_note

# select output folder
pmb.alert("Now you will choose the folder where the output will be saved.", "Output folder")
output_folder = tk.filedialog.askdirectory(initialdir = current_dir, title = "Choose output folder")
output_folder_rel = os.path.relpath(output_folder)

# choose output prefix
output_pre = pmb.prompt("Enter the prefix for your output", title= "Prefix", default="out")
output_folder_prefix = output_folder_rel + "/" + output_pre
base_set["output_prefix"] = output_folder_prefix

### PERMUTATION

# Permutation for prompts
perm_param_choice = pmb.confirm("Do you want to permutate prompts?", "Permutate Prompts?", ["Yes", "No"])

if perm_param_choice == "Yes":
    pmb.alert("Now you will choose the prompts to permutate over. "
        "Select ALL files that should be considered in the permutation in the next window (use ctrl / cmd).",
        "Prompts permutation")
    perm_prompts = tk.filedialog.askopenfilenames(initialdir = current_dir, title='Choose prompts')
    perm_prompts_rel = []
    for prompt in perm_prompts:
       prompt_rel = os.path.relpath(prompt)
       perm_prompts_rel.append(prompt_rel)
    base_set["permutations"][0]["prompt_filename"] = perm_prompts_rel

# Permutation for generation paramters
perm_param_choice = pmb.confirm("Do you want to permutate generation parameter?", "Permutate Generation Parameter?", ["Yes", "No"])

if perm_param_choice == "Yes":
    # Define tk Class for choosing permutation params:

    perm_picks_li = [] # list with picks for permutation will be filled with user choices

    class ChoosePerm(tk.Frame):
        def __init__(self,master=None,**kw):
            self.picks = {'model': 0, 'prefix': 0, 'temperature': 0, 'max_length': 0,'min_length': 0,
            'top_k': 0, 'top_p': 0, 'tail_free_sampling': 0,
            'repetition_penalty': 0, 'repetition_penalty_range': 0, 'repetition_penalty_slope': 0}
            tk.Frame.__init__(self,master=master,**kw)

            default_font = tk.font.nametofont("TkDefaultFont")
            default_font.configure(family="Arial", size=12)

            tk.Label(self,text="Chose Parameters to permutate (modify) over iterations").grid(row=0)
            row_nr = 1
            for key in self.picks:
                value = tk.IntVar()
                cb = tk.Checkbutton(self, text=key, offvalue=0, onvalue=1, variable = value)
                cb.grid(row=row_nr, sticky="W")
                row_nr += 1

                self.picks[key] = value

            tk.Button(self,text="Go",command = self.get_picks_vals).grid(row=11,column=1)

        def get_picks_vals(self):
            for key in self.picks:
                self.picks[key] = self.picks[key].get()
            list_picks(self.picks)
            self.master.destroy()

    def list_picks(pick_dict):
        for key in pick_dict:
            if pick_dict[key] == 1:
                perm_picks_li.append(key)

    root = tk.Tk()
    root.title("Choose Permutation Parameters")
    ChoosePerm(root).grid()
    root.mainloop()

    # Set permutation parameters
    for pick in perm_picks_li:
        user_input = pmb.prompt("Enter the values to use for the permutation for {}. Seperate values with ','".format(pick),
            title= pick, default=str(base_set["parameters"][pick]) + ", value2")
        input_li = user_input.split(",")
        base_set["permutations"][0][pick] = input_li

print(base_set)