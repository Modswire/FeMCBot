import subprocess, os
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from bot import FeMCBot

def download(extension):
    os.system(f"cd extensions && git clone https://gitlab.com/LiloviaLilossy/FeMCBot_{extension}.git")

def start(extension):
    run = eval(f"from extensions.FeMCBot_{extension} import run")
    run.setup(FeMCBot)

def get_data(extension):
    with open(f"extensions/FeMCBot_{extension}/data_info.txt", "r") as f:
        data = f.readlines()
        return data