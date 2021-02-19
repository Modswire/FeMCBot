import subprocess, os
from typing import TYPE_CHECKING

def download(extension):
    try: mkdir(f"extensions")
    except: pass
    os.system(f"cd extensions && git clone https://gitlab.com/LiloviaLilossy/FeMCBot_{extension}.git")

def start(extension, bot):
    run = exec(f"from extensions.FeMCBot_{extension} import run")
    run.setup(bot)

def get_data(extension):
    with open(f"extensions/FeMCBot_{extension}/data_info.txt", "r") as f:
        data = [i.rstrip("\n") for i in f.readlines()]
        return data