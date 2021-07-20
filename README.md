# nrt JSON Builder & Launcher
A little tool for using the [NovelAI Research Tool](https://github.com/wbrown/novelai-research-tool): A GUI to more easily build your input JSONs.

This tool consists of two parts: The `nrt JSON builder` and the `nrt Launcher`

# First Things First: What you need
* This tool is intended for windows users.
    * More specifically, the .exe files will only work for windows users. You can still use the python scripts ([nrt_json_builder.py](https://github.com/MWiechmann/nrt_json_builder/blob/main/nrt_json_builder.py) and [nrt_launcher.py](https://github.com/MWiechmann/nrt_json_builder/blob/main/nrt_launcher.py)) on any envrionment as long as you have all the dependencies.
* Obviously, you need a working version of the [NovelAI Research Tool](https://github.com/wbrown/novelai-research-tool)
* The easiest way to use this tool for windows users is to just download the exe files for the [nrt JSON Builder](https://github.com/MWiechmann/nrt_json_builder/blob/main/dist/nrt_json_builder.exe) and [nrt Launcher](https://github.com/MWiechmann/nrt_json_builder/blob/main/dist/nrt_launcher.exe)

# The nrt JSON Builder
The Json Builder provieds a GUI that you can use to build your Input-JSONs for `nrt`. Most feature of the current version of `nrt` (20-07-2021) are supported with the exception of running several permutation sets.

![Example Menu 1: Set Base Parameters](https://i.imgur.com/c3nnQnO.png)
![Example Menu 2: Choose Permutation Parameters](https://i.imgur.com/LqmKKMy.png)

The JSON Builder can also generate a config file that allows you to run `nrt` through the nrt Launcher.

# The nrt Launcher
Are you clinically averse to running programs through the command line? Fear not: Just start `nrt` with the nrt launcher! It takes an ini file with the location of your `nrt` install and the location of you JSON file and then starts up your test batch through `ntr`.

Okay...I admit must people will not need the functionality of the nrt Launcher. Right now it is just a stepping stone for some functionality I want to add soon™.
