import json
import os
import subprocess
import glob
import re
import copy
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

# General
nrt_file = config.get("General", "nrt_file")
json_file = config.get("General", "json_file")
out_dir = config.get("General", "out_dir")
outfile_pattern = config.get("General", "outfile_pattern")
# Recursive testing
do_recursive = config.getboolean("Recursive Testing", "do_recursive")
only_rec = config.getboolean("Recursive Testing", "only_rec")
delete_memory = config.getboolean("Recursive Testing", "delete_memory")
delete_an = config.getboolean("Recursive Testing", "delete_an")
addendum = config.get("Recursive Testing", "rec_addendum")
rec_json_base_str = config.get("Recursive Testing", "rec_json")
rec_json_base = json.loads(rec_json_base_str)
# add prefix for recurrent testing to json
rec_json_base["output_prefix"] = "rec"

# the JSON input uses file location relative to itself
# change working dir to json file location
os.chdir(os.path.dirname(json_file))

pmb.alert("Succesfully read in config file. Click Ok to start test batch.", "Start Test Batch")

if not only_rec:
    subprocess.check_call([nrt_file, json_file])

print("\n\nNOW STARTING WITH RECURSIVE TESTING\n\n")

if do_recursive:

    # create new folder for recursive outputs
    rec_out_dir = os.path.join(out_dir,"recursive_outputs")
    if not os.path.exists(rec_out_dir):
        os.mkdir(rec_out_dir)

    # Detect all output files from last run
    outputs_li = glob.glob(outfile_pattern)

    # Cycle through generated outputs
    for output in outputs_li:
        # determine diretorcy name for current output
        # extract just the filename without .json
        # theoretically possible with the os module
        # but there are some caveats to that so rather use a regex patterns
        file_name_without_json = re.sub(r".*\\","",output)
        file_name_without_json = re.sub(r".*\/","",file_name_without_json)
        file_name_without_json = file_name_without_json.replace(".json", "")
        current_out_dir = os.path.join(os.path.dirname(output), "recursive_outputs", file_name_without_json)
        # create current out dir
        if not os.path.exists(current_out_dir):
            os.mkdir(current_out_dir)

        # intialize current input_json
        current_input_json =  copy.deepcopy(rec_json_base)
        # read in current output file - skip if read error
        try:
            with open(output, encoding='utf-8') as output_file:
                output_json = json.loads(output_file.read())
        except:
            print("ERROR reading in {}. Skipping file.".format(output))
            continue

        # if current output is empty go on to next output
        if not output_json:
            continue

        # Set base context
        prompt = output_json[0]["prompt"]
        memory = output_json[0]["memory"]
        authors_note = output_json[0]["authors_note"]
        result = output_json[0]["result"]

        current_input_json["prompt"] = prompt + result + addendum
        current_input_json["memory"] = "" if delete_memory else memory
        current_input_json["authors_note"] = "" if delete_an else authors_note

        # Set permutations prompts
        if len(output_json) > 1:
            current_input_json["permutations"] = [{"prompt":[]}]

            i = 0
            for iteration in output_json:
                prompt = output_json[i]["prompt"]
                memory = output_json[i]["memory"]
                authors_note = output_json[i]["authors_note"]
                result = output_json[i]["result"]
                
                current_input_json["permutations"][0]["prompt"].append(prompt + result + addendum)

                i += 1

        # save json file for current output
        current_json_location = os.path.join(current_out_dir, "_recursive_input.json")

        with open(current_json_location, 'w') as file:
            json.dump(current_input_json, file, indent=4)

        # run recursive test
        subprocess.check_call([nrt_file, current_json_location])

pmb.alert("Done with test batch!", "Test Batch Done!")