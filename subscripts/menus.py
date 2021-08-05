import os
import tkinter as tk
from functools import partial

def clean_text_input(text_input):
    """tkinter adds \n to the end of Text fields.
    This is a simple function to remove these.
    """
    return text_input[:-1] if text_input.endswith("\n") else text_input

class BaseSet(tk.Frame):
    """Menu to add the Base Settings for direct testing.
    Needs to a dict with settings to be passed (settings_json) to save settings to.
    Takes input for: prompt_filename or scenario_filename,
    memory, authors_note, output_prefix, iterations, generations
    """
    def __init__(self,master=None, settings_json={}, json_dir = "C:", **kw):
        # intialize self.json_dir (needed for functions)
        self.json_dir = json_dir

        # populate self.settings
        # check if the settings_json has the necessary keys
        # fill entries for missing keys
        settings_json_keys =  ["prompt_filename", "memory", "authors_note", "output_prefix", "iterations", "generations"]
        self.settings = {}
        for key in settings_json_keys:
            # make sure it can be either prompt_filename or scenario_filename
            if key == "prompt_filename":
                if "prompt_filename" in settings_json:
                    self.settings["prompt_filename"] = settings_json["prompt_filename"]
                elif "scenario_filename" in settings_json:
                    self.settings["prompt_filename"] = settings_json["scenario_filename"]
                else:
                    self.settings["prompt_filename"] = ""
            elif key in settings_json:
                self.settings[key] = settings_json[key]
            else:
                self.settings[key] = ""

        self.items = {} # will be used to store/reference most entry widgets

        tk.Frame.__init__(self,master=master, **kw)

        default_font = tk.font.nametofont("TkDefaultFont")
        default_font.configure(family="Arial", size=12)

        tk.Label(self,text="Chose Base Settings").grid(row=0, sticky="E")
        row_nr = 1

        value = tk.StringVar()

        for key in self.settings:
            if (key == "prompt_filename") or (key == "scenario_filename"):
                self.prompt_type = key
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
        tk.Button(self,text="Ok",command = partial(self.adjust_base_settings, settings_json)).grid(row=row_nr,column=1)

    def set_prompt(self):
        if self.prompt_type == "prompt_filename":
            file_type = (("txt files","*.txt"),("all files","*.*"))
        else:
            file_type = (("scenario files","*.scenario"),("all files","*.*"))

        base_prompt_abs = tk.filedialog.askopenfilename(initialdir = self.json_dir,
            title = "Choose base prompt",
            filetypes = (file_type))
        self.settings[self.prompt_type] = os.path.relpath(base_prompt_abs, start = self.json_dir)
        self.prompt_txt.configure(text=self.settings[self.prompt_type])
        
    def set_out_dir(self):
        global out_dir_abs
        out_dir_abs = tk.filedialog.askdirectory(initialdir = self.json_dir, 
            title = "Choose output folder")
        self.out_dir_rel = os.path.relpath(out_dir_abs, start = self.json_dir)
        self.update_out_txt()
        
    def update_out_txt(self):
        self.out_pre = self.out_pre_enter.get()
        comb_out = os.path.join(self.out_dir_rel, self.out_pre)
        self.settings["output_prefix"] = comb_out
        self.out_dir_pre_txt.configure(text = self.settings["output_prefix"])
        return True

    def adjust_base_settings(self, settings_json):
        """ get responses from items (that have not been handled yet)
        and store in self.settings
        """
        setting_types_dict = {"prompt_filename": str, "memory": str, "authors_note": str,
        "output_prefix":str, "iterations": int, "generations": int}
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
                setting_type = setting_types_dict[key]
                if (setting_type == str) or (value == ""): 
                # empty values are handled in  the next step
                # for now just transfer them over
                    self.settings[key] = value
                elif setting_type == int:
                    self.settings[key] = int(value)
                else:
                    print("WARNING! Transformation missing for {} into {} for BaseParams".format(key, str(setting_type)))

        for key in self.settings:
            if self.settings[key] == "":
                # nrt handels missing fields fine so the cleanest solution is to just to delete the key
                settings_json.pop(key, None)
            else:
                settings_json[key] = self.settings[key]
        self.master.destroy()
        self.quit()

class BaseParams(tk.Frame):
    """Menu to add the Base Parameters for direct testing
    Needs to a dict with settings to be passed (settings_json) to save settings to.
    Takes input for: model, prefix, temperature, max_length, min_length,
    top_k, top_p, tail_free_sampling, repetition_penalty, repetition_penalty_range,
    repetition_penalty_slope, bad_words_ids, ban_brackets
    """
    def __init__(self,master=None, settings_json={}, **kw):


        # populate self.params
        # check if the settings_json has the necessary keys
        # fill entries for missing keys
        params_json_keys =  ["model", "prefix", "temperature", "max_length", "min_length",
        "top_k", "top_p", "tail_free_sampling", "repetition_penalty", "repetition_penalty_range",
        "repetition_penalty_slope", "bad_words_ids", "ban_brackets"]
        self.params = {}
        # if there is no parameters entry in the json_dict just fill in everything with blanks
        if "parameters" not in settings_json:
            for key in params_json_keys:
                self.params[key] = ""
        # if there is a parameters entry, copy over the specific parameters
        # if a parameter is missing fill in with blank tring
        else:
            for key in params_json_keys:
                if key in settings_json["parameters"]:
                    self.params[key] = settings_json["parameters"][key]
                else:
                    self.params[key] = ""

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

        tk.Button(self,text="Ok",command = partial(self.adjust_base_params, settings_json)).grid(row=row_nr,column=1, sticky="E")

    def adjust_base_params(self, settings_json):
        """ get responses from items (that have not been handled yet)
        and store in self.params
        """

        setting_types_dict = {"model":str, "prefix":str, "temperature":float, "max_length":int, "min_length":int,
        "top_k":int, "top_p":float, "tail_free_sampling":float, "repetition_penalty":float, "repetition_penalty_range":int,
        "repetition_penalty_slope":float, "bad_words_ids":list, "ban_brackets":bool}

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
                setting_type = setting_types_dict[key]
                if setting_type == str or (value == ""):
                    # empty values are handled by nrt so no problem to just transfer them over
                    self.params[key] = value
                elif setting_type == int:
                    self.params[key] = int(value)
                elif setting_type == float:
                    self.params[key] = float(value)
                else:
                    print("WARNING! Transformation missing  for {} into {} for BaseParams".format(key, str(setting_type)))

        for key in self.params:
            if self.params[key] == "":
                # nrt handels missing fields fine so the cleanest solution is to just to delete the key
                settings_json["parameters"].pop(key, None)
            else:
                settings_json["parameters"][key] = self.params[key]
        self.master.destroy()
        self.quit()

class ChoosePerm(tk.Frame):
    """Menu to choose the variables to be permutated in direct testing
    Need an empty list to be passed (perm_picks_li) to save choices to.
    perm_picks_li will be emptied before choices are saved into it!
    Possible choices for permutation: prompt_filename, memory, authors_note, model, prefix, 
    temperature, max_length,min_length, top_k, top_p, tail_free_sampling,
    repetition_penalty, repetition_penalty_range, repetition_penalty_slope
    """
    def __init__(self,master=None, perm_picks = [], **kw):
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

        tk.Button(self,text="OK",command = partial(self.get_picks_vals, perm_picks)).grid(row=row_nr,column=1, sticky="E")

    def get_picks_vals(self, perm_picks):
        del perm_picks[:]

        for key in self.items:
            self.picks[key] = self.items[key].instate(["selected"])
            if self.picks[key]:
                perm_picks.append(key)
        print(perm_picks)
        self.master.destroy()
        self.quit()
