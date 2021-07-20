import json
import copy
import os 
import tkinter as tk
from tkinter import font
from tkinter import filedialog
from tkinter import ttk
import pymsgbox as pmb
from configparser import ConfigParser

# set json contents (use default for now)
json_content = { 
  "prompt_filename": "prompt.txt",
  "memory": "",
  "authors_note": "",
  "output_prefix": "outputs/out",
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

# Initialize Json file
pmb.alert("First you need to choose the file location for your JSON input file.\nThe ending '.json' will be automatically appended", "Base Prompt")
current_dir = os.path.dirname(os.path.realpath(__file__))
json_file = tk.filedialog.asksaveasfilename(initialdir = current_dir,
    title = "Choose JSON file location", defaultextension=".json",
    filetypes = (("json files","*.json"),("all files","*.*")))
json_dir = os.path.dirname(json_file)

scenario_choice = pmb.confirm("Do you want to use txt prompts or a scenario file for the base settings?", "Use scneario file?", [".txt file", ".scneario file"])

if scenario_choice == ".scneario file":
    json_content["scenario_filename"] = json_content.pop("prompt_filename")
    json_content["scenario_filename"] = "scenario.scenario"

# MENU 1 : Enter Base Settings
class BaseSet(tk.Frame):
    def __init__(self,master=None,**kw):
        self.settings = copy.deepcopy(json_content)
        self.settings.pop('parameters', None)
        self.settings.pop('permutations', None)

        self.items = {} # will be used to store/reference most entry widgets

        tk.Frame.__init__(self,master=master,**kw)

        default_font = tk.font.nametofont("TkDefaultFont")
        default_font.configure(family="Arial", size=12)

        tk.Label(self,text="Chose Base Settings").grid(row=0, sticky="E")
        row_nr = 1

        value = tk.StringVar()

        for key in self.settings:
            if (key == "prompt_filename") or (key == "scenario_filename"):
                # Browse Button for Base Prompt/Scenario
                # has its own handling and is thus not stored in self.items
                tk.Label(self,text=key).grid(row=row_nr,column=0, sticky="E")
                tk.Button(self,text="Browse", command = self.set_prompt).grid(row=row_nr,column=1, sticky = "W")
                row_nr += 1
                # Text displaying current Base Prompt
                self.prompt_txt = tk.Label(self,text=self.settings[key])
                self.prompt_txt.grid(row=row_nr,column=1, sticky="W")
            elif key == "output_prefix":
                # Output Folder
                # has its own handling and is thus not stored in self.items
                self.out_dir_rel = "outputs"
                tk.Label(self,text="Output Folder").grid(row=row_nr,column=0, sticky="E")
                tk.Button(self,text="Browse", command = self.set_out_dir).grid(row=row_nr,column=1, sticky = "W")
                row_nr += 1
                # Outfile Prefix
                tk.Label(self,text="Prefix for Output Files").grid(row=row_nr,column=0, sticky="E")
                self.out_pre_enter = tk.Entry(self, font=('Arial', 11),
                    validate = "focus", validatecommand = self.update_out_txt)
                self.out_pre_enter.insert(0, "out")
                self.out_pre_enter.grid(row=row_nr,column=1, sticky = "W")
                row_nr+= 1
                # Text displaying current combined Out Prefix
                self.out_dir_pre_txt = tk.Label(self,text=self.settings["output_prefix"])
                self.out_dir_pre_txt.grid(row=row_nr,column=1, sticky="W")
            elif key == "memory":
                tk.Label(self,text=key).grid(row=row_nr,column=0, sticky="E")
                self.items[key] = tk.Text(self, font=('Arial', 10), height = 5, width = 30)
                self.items[key].insert("end", self.settings[key])
                self.items[key].grid(row=row_nr,column=1, sticky = "W")
            elif key == "authors_note":
                tk.Label(self,text=key).grid(row=row_nr,column=0, sticky="E")
                self.items[key] = tk.Text(self, font=('Arial', 10), height = 3, width = 30)
                self.items[key].insert("end", "[ Author: ; Tags: ; Genre: ]")
                self.items[key].grid(row=row_nr,column=1, sticky = "W")
            else:
                tk.Label(self,text=key).grid(row=row_nr,column=0, sticky="E")
                self.items[key] = tk.Entry(self, font=('Arial', 11))
                self.items[key].insert(0, self.settings[key])
                self.items[key].grid(row=row_nr,column=1, sticky = "W")
            row_nr += 1
        tk.Button(self,text="Ok",command = self.adjust_base_settings).grid(row=row_nr,column=1)

    def set_prompt(self):
        if scenario_choice == ".txt file":
            key = "prompt_filename"
            file_type = (("txt files","*.txt"),("all files","*.*"))
        else:
            key = "scenario_filename"
            file_type = (("scenario files","*.scenario"),("all files","*.*"))

        base_prompt_abs = tk.filedialog.askopenfilename(initialdir = json_dir,
            title = "Choose base prompt",
            filetypes = (file_type))
        self.settings[key] = os.path.relpath(base_prompt_abs, start = json_dir)
        self.prompt_txt.configure(text=self.settings[key])
        
    def set_out_dir(self):
        out_dir_abs = tk.filedialog.askdirectory(initialdir = json_dir, 
            title = "Choose output folder")
        self.out_dir_rel = os.path.relpath(out_dir_abs, start = json_dir)
        self.update_out_txt()
        
    def update_out_txt(self):
        self.out_pre = self.out_pre_enter.get()
        comb_out = os.path.join(self.out_dir_rel, self.out_pre)
        self.settings["output_prefix"] = comb_out
        self.out_dir_pre_txt.configure(text = self.settings["output_prefix"])
        return True

    def adjust_base_settings(self):
        # update values for memory & author's note
        #tkinter adds \n to the end of Text fields, remove these first

        # get responses from items (that have not been handled yet)
        # and store in self.settings
        for key in self.items:
            if key == "memory":
                memory_clean = clean_text_input(self.items["memory"].get("1.0","end"))
                self.settings["memory"] = memory_clean
            elif key == "authors_note":
                authors_note_clean = clean_text_input(self.items["authors_note"].get("1.0","end"))
                self.settings["authors_note"] = authors_note_clean
            else:
                value = self.items[key].get() # get response (as string)
                # transform into correct type, then store
                setting_type = type(self.settings[key])
                if (setting_type == str) or (value == ""): 
                # empty values are handled by nrt so no problem to just transfer them over
                    self.settings[key] = value
                elif setting_type == int:
                    self.settings[key] = int(value)
                else:
                    print("WARNING! Transformation missing  for {} into {} for BaseParams".format(key, str(setting_type)))

            for key in self.settings:
                json_content[key] = self.settings[key]
        self.master.destroy()
        self.quit()

def clean_text_input(text_input):
    return text_input[:-1] if text_input.endswith("\n") else text_input

root = tk.Tk()
root.title("Set Base Settings")
BaseSet(root).grid()
root.mainloop()

# MENU 2: Enter Base Parameters:
class BaseParams(tk.Frame):
    def __init__(self,master=None,**kw):
        self.params = copy.deepcopy(json_content["parameters"])
        self.params.pop('use_cache', None)
        self.params.pop('use_string', None)
        self.params.pop('return_full_text', None)

        self.items = {} # will be used to store/reference the entry widgets
        
        tk.Frame.__init__(self,master=master,**kw)

        default_font = tk.font.nametofont("TkDefaultFont")
        default_font.configure(family="Arial", size=12)

        tk.Label(self,text="Chose Base Parameters").grid(row=0, sticky="E")
        row_nr = 1
        for key in self.params:
            if key == "bad_words_ids":
                tk.Label(self,text="Bad words IDs. Seperate IDs with `,`.").grid(row=row_nr,column=0, sticky="E")
                self.items[key] = tk.Entry(self, font=('Arial', 12))
                self.items[key].grid(row=row_nr,column=1)
            elif key == "ban_brackets":
                tk.Label(self,text="Ban bracket generation").grid(row=row_nr,column=0, sticky="E")
                self.items[key] = tk.ttk.Checkbutton(self, text="", takefocus=False)
                self.items[key].grid(row=row_nr, column = 1, sticky="W")
                self.items[key].invoke()
            else:
                tk.Label(self,text=key).grid(row=row_nr,column=0, sticky="E")
                self.items[key] = tk.Entry(self, font=('Arial', 12))
                self.items[key].insert(0, self.params[key])
                self.items[key].grid(row=row_nr,column=1)

            row_nr += 1

        tk.Button(self,text="Ok",command = self.adjust_base_params).grid(row=row_nr,column=1, sticky="E")

    def adjust_base_params(self):
        # store entries in self.params
        for key in self.items:
            
            if key == "bad_words_ids":
                value = self.items[key].get() # get response (as string)
                if value == "":
                    self.params[key] = []
                else:
                    value = value.split(",")
                    self.params[key] = [int(item) for item in value]
            elif key == "ban_brackets":
                self.params[key] = self.items[key].instate(["selected"])
            else:
                value = self.items[key].get() # get response (as string)
                # transform into correct type, then store
                setting_type = type(self.params[key])
                if setting_type == str:
                    self.params[key] = value
                elif setting_type == int:
                    self.params[key] = int(value)
                elif setting_type == float:
                    self.params[key] = float(value)
                else:
                    print("WARNING! Transformation missing  for {} into {} for BaseParams".format(key, str(setting_type)))

        for key in self.params:
            json_content["parameters"][key] = self.params[key]
        self.master.destroy()
        self.quit()

root = tk.Tk()
root.title("Set Base Parameters")
BaseParams(root).grid()
root.mainloop()

### PERMUTATION

# Menu 3: Select Vars for Permutation for prompts

perm_picks_li = [] # list with picks for permutation will be filled with user choices

class ChoosePerm(tk.Frame):
    def __init__(self,master=None,**kw):
        self.picks = {'prompt_filename': False, 'memory': False, 'authors_note': False, 'model': False, 'prefix': False, 'temperature': False, 'max_length': False,'min_length': False,
        'top_k': False, 'top_p': False, 'tail_free_sampling': False,
        'repetition_penalty': False, 'repetition_penalty_range': False, 'repetition_penalty_slope': False}
        tk.Frame.__init__(self,master=master,**kw)

        self.items = {} # will be used to store/reference the entry widgets

        default_font = tk.font.nametofont("TkDefaultFont")
        default_font.configure(family="Arial", size=12)

        tk.Label(self,text="Chose Parameters to permutate (modify) over iterations").grid(row=0)
        row_nr = 1
        for key in self.picks:
            self.items[key] = tk.ttk.Checkbutton(self, text=key, takefocus=False)
            self.items[key].grid(row=row_nr, sticky="W")
            self.items[key].invoke()
            self.items[key].invoke()
            row_nr += 1

        tk.Button(self,text="OK",command = self.get_picks_vals).grid(row=row_nr,column=1, sticky="E")

    def get_picks_vals(self):
        for key in self.items:
            self.picks[key] = self.items[key].instate(["selected"])
            if self.picks[key]:
                perm_picks_li.append(key)
        self.master.destroy()
        self.quit()

root = tk.Tk()
root.title("Choose Permutation Parameters")
ChoosePerm(root).grid()
root.mainloop()

# Menu 4: Set permutation parameters

class SetPermParams(tk.Frame):
    def __init__(self,master=None,**kw):
        self.perm = {} # stores permutation parameters

        self.items = {} # will be used to store/reference the entry widgets
        
        tk.Frame.__init__(self,master=master,**kw)

        default_font = tk.font.nametofont("TkDefaultFont")
        default_font.configure(family="Arial", size=12)

        tk.Label(self,text="Enter the values to use for the permutation. Seperate values with ','.\n\
            Excpetion: Seperate with `,,` for memory and authors_note")\
        .grid(row=0, sticky="W", columnspan=2)

        row_nr = 1
        for pick in perm_picks_li:
            if pick == "prompt_filename":
                try:
                    self.perm[pick] = json_content[pick] # copy value from base settings
                except:
                    self.perm[pick] = "prompt.txt" # if base setting uses scenario there will be no prompt name to opy
                # also add base prompt to permutation list (in case users does never hits browse button)
                json_content["permutations"][0]["prompt_filename"] = self.perm[pick]
                # Browse Button for Base Prompt
                # has its own handling and is thus not stored in self.items
                tk.Label(self,text="Pick Prompts").grid(row=row_nr,column=0, sticky="E")
                tk.Button(self,text="Browse", command = self.set_perm_prompts).grid(row=row_nr,column=1, sticky = "W")
                row_nr += 1
                # Text displaying current Base Prompt
                self.prompt_txt = tk.Label(self,text=self.perm["prompt_filename"])
                self.prompt_txt.grid(row=row_nr,column=1, sticky="W")    
            elif (pick == "memory") or (pick == "authors_note"):
                self.perm[pick] = json_content[pick] # copy value from base settings
                tk.Label(self,text="IMPORTANT! For {} values should be seperated by ',,' instead of ','."\
                    .format(pick)).grid(row=row_nr,column=0, sticky="W", columnspan=2)
                row_nr += 1
                tk.Label(self,text=pick).grid(row=row_nr,column=0, sticky="E")
                self.items[pick] = tk.Text(self, font=('Arial', 10), height = 5, width = 30)
                self.items[pick].insert("end", json_content[pick])
                self.items[pick].grid(row=row_nr,column=1, sticky = "W")
            else:
                self.perm[pick] = json_content["parameters"][pick] # copy value from base settings
                tk.Label(self,text=pick).grid(row=row_nr,column=0, sticky="E")
                self.items[pick] = tk.Entry(self, font=('Arial', 12))
                default_text = str(json_content["parameters"][pick]) + ", value2, ..."
                self.items[pick].insert(0, default_text)
                self.items[pick].grid(row=row_nr,column=1, sticky = "W")
            row_nr += 1

        tk.Button(self,text="Ok",command = self.adjust_perm_params).grid(row=row_nr,column=1, sticky="E")

    def set_perm_prompts(self):
        pmb.alert("Now you will choose the prompts to permutate over. "
            "Select ALL files that should be considered in the permutation in the next window (use ctrl / cmd).",
            "Prompts permutation")

        perm_prompts_abs = tk.filedialog.askopenfilenames(initialdir = json_dir, title='Choose prompts',
            filetypes = (("txt files","*.txt"),("all files","*.*")))
        perm_prompts_rel = []

        for prompt in perm_prompts_abs:
            prompt_rel = os.path.relpath(prompt, start = json_dir)
            perm_prompts_rel.append(prompt_rel)
        # Update value in json_content
        self.perm["prompt_filename"] = perm_prompts_rel
        json_content["permutations"][0]["prompt_filename"] = self.perm["prompt_filename"]
        # Update text on menu
        txt = "\n".join(perm_prompts_rel)
        self.prompt_txt.configure(text=txt)

    def adjust_perm_params(self):
    #  store entries in self.params
        for key in self.items:

            # make list from string - special treatment for memory & author's note
            if (key == "memory") or (key == "authors_note"):
                value = clean_text_input(self.items[key].get("1.0","end"))
                delimiter = ",,"
            else:
                value = self.items[key].get() # get response (as string)
                delimiter = ","
            
            if value == "":
                self.perm[key] = []
            else:
                value = value.split(delimiter)

                # transform into correct type and store
                setting_type = type(self.perm[key])
                if setting_type == str:
                    self.perm[key] = value
                elif setting_type == int:
                    self.perm[key] = [int(item) for item in value]
                elif setting_type == float:
                    print(value)
                    self.perm[key] = [float(item) for item in value]
                else:
                    print("WARNING! Transformation missing  for {} into {} for SetPermParams".format(key, str(setting_type)))
            json_content["permutations"][0][key] = self.perm[key]
        self.master.destroy()
        self.quit()

root = tk.Tk()
root.title("Set Permutation Parameters")
SetPermParams(root).grid()
root.mainloop()

with open(json_file, 'w') as file:
    json.dump(json_content, file, indent=4)

config_creation_choice = pmb.confirm("I have written your settings to the json file.\n" 
    "If you would like to use the nrt launcher please cotinue to create a config file for it", 
    "Create Launcher Config?", ["Nah I am good... (Leave)", "Continue to config file"])

if config_creation_choice == "Nah I am good... (Leave)":
    exit()

# Set nrt location
# Try to automatically look for nrt (based on json location)
# Look in json_dir
if os.path.isfile(os.path.join(json_dir, "nrt.exe")):
    nrt_file = (os.path.join(json_dir, "nrt.exe"))
elif os.path.isfile(os.path.join(os.path.dirname(json_dir), "nrt.exe")):
    nrt_file = (os.path.join(os.path.dirname(json_dir), "nrt.exe"))
else:
    pmb.alert("Could not find nrt.exe.\nPlease indicate location of nrt.exe in the following screen.", "Indicate location of nrt.exe")
    nrt_file = tk.filedialog.askopenfilename(initialdir = json_dir,
        title = "Indicate location of nrt.exe", filetypes = (("nrt.exe","nrt.exe"),("all files","*.*")))

# Write settings to file
pmb.alert("Please indicate where the setting should be stored. The ending '.ini' will be automatically appended to the filename.",
    "Store settings")
config_file = tk.filedialog.asksaveasfilename(initialdir = json_dir,
    title = "Choose config file location", defaultextension=".ini",
    filetypes = (("ini files","*.ini"),("all files","*.*")))

config = ConfigParser()
config.add_section("General")
config.set("General", "nrt_file", nrt_file)
config.set("General", "json_file", json_file)

with open(config_file, 'w') as f:
    config.write(f)

pmb.alert("I have written the settings for the nrt launcher to file. Now exiting the program.",
    "All Done!")