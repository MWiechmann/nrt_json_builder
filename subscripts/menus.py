import os
import tkinter as tk
from functools import partial

def clean_text_input(text_input):
    """tkinter adds \n to the end of Text fields.
    This is a simple function to remove these.
    """
    return text_input[:-1] if text_input.endswith("\n") else text_input

class BaseSet(tk.Frame):
    """Menu to add the Base Settings for direct testing
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
                settings_json.pop(key)
            else:
                settings_json[key] = self.settings[key]
        self.master.destroy()
        self.quit()

