#!/usr/bin/env python
__version__ = "1.0.0"
import os, subprocess, sys, stat, shutil, requests as r
from pathlib import Path
from colorama import Fore

w = Fore.WHITE
bl = Fore.BLACK
rd = Fore.RED
gr = Fore.GREEN
ylw = Fore.YELLOW
reset = Fore.RESET

def run_cmd(cmd):
    subprocess.run(cmd, shell=True, check=True)

def refresh():
    url = "https://raw.githubusercontent.com/wxwreak/ppurge/refs/heads/main/ppurge.py"
    resp = r.get(url)
    if resp.status_code == 200:
        with open("ppurge.py", "wb") as f:
            f.write(resp.content)
        print("Succesfully fetch update")
    else:
        print("Failed to fetch update")
        return
    ppurge_f = "ppurge.py"
    ppurge_alias = "ppurge"
    target = Path.home() / ".local" / "bin"
    target.mkdir(parents=True, exist_ok=True)
    st = os.stat(ppurge_f)
    os.chmod(ppurge_f, st.st_mode | stat.S_IEXEC)
    shutil.copy(ppurge_f, target / ppurge_alias)
    print(f"{ppurge_f} refreshed")

def show_ver():
    print(f"Version: [{__version__}]")

def ppurge():
    if not os.path.exists(".git"):
        print(f"{bl}[{w}!{bl}] {rd}Error: Current directory is not a git repository (no .git folder found){reset}")
        return

    clear_history = input("Do you also want to delete the history? [y/n]: ").lower()
    if clear_history == "y":
        print(f"{bl}[{w}Info{bl}] {ylw}Clearing history and repo{reset}")
        try:
            run_cmd("git rm -rf .")
            run_cmd("rm -rf .git")
            run_cmd("git init")
        except subprocess.CalledProcessError as e:
            print(f"{bl}[{w}!{bl}] {rd}Error during git operations: {e}{reset}")
            return

        with open(".gitignore", "w") as f:
            f.write("*.log")
        run_cmd("git add .gitignore")
        run_cmd("git commit -m 'Purge: cleanup files and history'")
        run_cmd("git push origin main --force")
        print(f"{bl}[{w}Success{bl}] {gr} Repo cleaned up & Synchronized{reset}")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        ppurge()
    else:
        arg = sys.argv[1]
        
        if arg == "--refresh":
            refresh()
        elif arg == "--help":
            commands = f"""
[ppurge] Standard ppurge for a utility to clean up Git history and synchronize the repository
ppurge [--help] Show this help message
ppurge [--refresh] Fetch new version from Github
ppurge [--version] Shows current version
            """
            print(commands)
        elif arg == "--version":
            show_ver()
        else:
            ppurge()
