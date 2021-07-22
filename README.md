# nrt JSON Builder & Launcher
A little tool for using the [NovelAI Research Tool](https://github.com/wbrown/novelai-research-tool): A GUI to more easily build your input JSONs. Also enables mass recursive testing with nrt.

This tool consists of two parts: The `nrt JSON builder` and the `nrt Launcher`

# First Things First: What you need
* This tool is intended for windows users.
    * More specifically, the .exe files will only work for windows users. You can still use the python scripts ([nrt_json_builder.py](https://github.com/MWiechmann/nrt_json_builder/blob/main/nrt_json_builder.py) and [nrt_launcher.py](https://github.com/MWiechmann/nrt_json_builder/blob/main/nrt_launcher.py)) on any envrionment as long as you have all the dependencies.
* Obviously, you need a working version of the [NovelAI Research Tool](https://github.com/wbrown/novelai-research-tool)
* The easiest way to use this tool for windows users is to just download the exe files for the [nrt JSON Builder](https://github.com/MWiechmann/nrt_json_builder/blob/main/dist/nrt_json_builder.exe) and [nrt Launcher](https://github.com/MWiechmann/nrt_json_builder/blob/main/dist/nrt_launcher.exe)

# The nrt JSON Builder
The Json Builder provieds a GUI that you can use to build your Input-JSONs for `nrt`. Most features of the current version of `nrt` (20-07-2021) are supported with the exception of running several permutation sets.

![Example Menu 1: Set Base Parameters](https://github.com/MWiechmann/nrt_json_builder/blob/main/example%20images/set_base_prompt.png)

The JSON Builder can also generate a config file that allows you to run `nrt` through the nrt Launcher. If you create a config file you also have the choice to enable mass recursive testing (see below).

# The nrt Launcher
Are you clinically averse to running programs through the command line? Fear not: Just start `nrt` with the nrt launcher! It takes an ini file with the location of your `nrt` install and the location of you JSON file and then starts up your test batch through `nrt`.

However, there is a another purpose to the nrt Launcher: It enables you to use `nrt` for automatic recursive testing.

# Automatic Recursive Testing
Most people running their own testing on NAI have experienced that confirmation bias is real. Is `Genre: Fantasy` really better than `Genre: fantasy` in [Author's Note](https://github.com/TravellingRobot/NAI_Community_Research/wiki/Author's-Notes-for-v3)? Does `tone: zany` *really* do anything? Or are you just kidding yourself when evaluating the outputs?

Sometimes it would be nice to be able to quickly ask someone "Hey, what genre do you think this is?", ideally someone that is blind to your testing conditions. Well, why not just do exactly that with Sigurd?

This is the idea of recursive testing - you take the output from your `nrt` test set, modify it and then feed the whole thing back into the AI as input. Usually you will edit out your context manipulation (like A/N or memory) to make the test "blind" and add an evaluation question for the AI to evaluate the success of your manipulation. The following example should hopefully make clearer how this works in practice.

## Recursive Testing Example
Let's say you want to see if there is any difference between `Genre: scifi`, `Genre: SciFi`, `Genre: science fiction` and `Genre: Science Fiction`. You also want to know how well these keywords work in general for activating recognizable SciFi tropes. This is an example where you can use mass recursive testing.

### Step 1: Generate Input Json for the Original Test
* Launch [nrt_json_builder.exe](...) to build the json for the first (original/standard) test batch. For this example I used default settings with 10 iterations and 15 generations each. But obviously you could set your preferred setting for sampling here.
* For the permutations parameters, I chose `authors_note` since we want to test different variations of author's note. For my tests, I like to also permutate over a set of different minimal prompts so I chose `prompt_filename` as an additional permutation paramter
![Picking Base Permutation Parameters](...)
* In the next window I set my selection of prompts and variations of author's note to permutate over. Make sure to include a control to rate the performance against! (In this case the control would be `[ Author: ; Tags: ; Genre: ]`).
    * For this example I pasted the follwoing set of author's notes:
    ```
    [ Author: ; Tags: ; Genre: ],,[ Author: ; Tags: ; Genre: scifi ],,[ Author: ; Tags: ; Genre: SciFi ],,[ Author: ; Tags: ; Genre: science fiction ],,[ Author: ; Tags: ; Genre: Science Fiction ]
    ```
![Setting Base Permutation Parameters](...)
* The Builder will save your settings to the input JSON and ask you if you want to create a config. Confirm and chose a file location of your choice.

### Step 2: Entering Settings for Recursive Testing
* When asked if you want to do recursive testing, confirm.
![I choose you recursive testing](...)
* The Builder offers to delete the original author's note and/or memory before feeding the output back to Sigurd. In this case `memory` was empty so the choice for memory does not matter. However, I definetly want to blind Sigurd about the original `authors_note` so I chose to delete it before recursive testing.
![Make Sigurd forget about the authors note](...)
* The Builder offers to add an addendum that is inserted at the end of the original output before it is fed back to the AI. In this case I want to see if Sigurd can recognize the genre of the text he wrote himself. So I enter an evaluation question about the genre.
![Tell me what you think Siggy](...)
* Finally the Builder wants to know what the generation setting during the recursive testing should be. I would not go too crazy on the generations and iterations here: Each single output will become its own input json with each iteration as its own permutation so better to keep it small.
![Keep it low numbers here](...)
* For the Parameters I wanted to know what is "on top of Sigurd's mind" when I ask him about the genre of the story, so I set top-k to 1.
![May the best token win](...)
* That's it - the Builder will save these settings for you to an ini-file and close.

One quick note about the ini-file: It will have a setting in there that reads `only_rec = False`. The builder will always be set to `False`. However, sometimes you might already have generated the original outputs and skip straight to the recursive testing (for example if you had to abort recursive testing for some reason). In that case you can set `only_rec = True` in the ini-file. This will make the Launcher skip straight to the recursive tests.

### Step 3: Run your tests!
* Start [nrt_launcher.exe](...) and load in the ini-file you just created with the launcher. The launcher should take everything from here. It will first fire up `nrt` to run the original tests and then use the generated outputs to generate *new* input json to feed to `nrt` for the recursive tests. This will take a while - just take a walk or something...
* Note: In some rare cases it can happen that some oddity in the original output prevents the Launcher from reading in the file and create the input JSON. In that case the specific output will be skipped and the Launcher will move on the next file.

### Step 4 Examine your results
* Your output folder will have the original outputs as usual. But you will see a folder for the recursive tests in there as well.
![Oh look what is that folder](...)
* When you open the folder for the recursive tests you will see that the Launcher created new folder for each original output file.
![So many folders](...)
* In each folder you will find:
    * The input JSON used for this part of the recursive test (called `_recursive_input.json`)
    * `nrt`'s output files. Each iteration of each output file will have its own output file.
![Inside of a recursive folder](...)
* Examine the results as you see fit 
    * For this example I could count up how often Siggy recognizes his writing as SciFi:
        * control: scifi: 30/40, SciFi: 33/40, science fiction: 32/40, Science Fiction :29/40
        * If you want you can even test the significance of the difference in proportions
            * To compute your p-value you can use [this online tool](https://www.socscistatistics.com/tests/ztest/default2.aspx) or [this one](https://www.medcalc.org/calc/comparison_of_proportions.php). But you should make sure that to also control for multiple testing before drawing any conclusions! You can use an online tool like [this one](https://tools.carbocation.com/FDR) to apply the Benjamini-Hochberg correction for mutliple testing (I would recommend to settle for an FDR of 0.1 for typical non-essential testing)
            * In this example all keywords performed clearly better than the control (*corrected ps* < 001. There were no differences in performance between the keywords.