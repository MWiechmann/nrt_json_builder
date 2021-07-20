import json
import os
import subprocess
import tkinter as tk
from tkinter import filedialog
import pymsgbox as pmb
from configparser import ConfigParser


# Load in settings from ini file
current_dir = os.path.dirname(os.path.realpath(__file__))

pmb.alert("In the following screen please select the config file for your test batch", "Indicate location of ini file")
config_file = tk.filedialog.askopenfilename(initialdir = current_dir,
    title = "Location of config file", filetypes = (("config file","*.ini"),("all files","*.*")))

config = ConfigParser()
config.read(config_file)

nrt_file = config.get("General", "nrt_file")
json_file = config.get("General", "json_file")

# the JSON input uses file location relative to itself
# change working dir to json file location
os.chdir(os.path.dirname(json_file))

pmb.alert("Succesfully read in config file. Click Ok to start test batch.", "Start Test Batch")

subprocess.check_call([nrt_file, json_file])

pmb.alert("Done with test batch!", "Test Batch Done!")