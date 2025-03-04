import run
import sys
import json

with open("./repl_settings.json") as repl_settings:
    settings = json.loads(repl_settings.read())

def run_repl():
    print("CySPL REPL, write $!help for commands")
    while 1:
        inp = input("> ")
        if inp.startswith("$!"):
            cmd_res = run_command(inp)
            if cmd_res == ("EXIT"): return
            continue
        res = run.run(inp, settings["max_comp_stage"])
        if res[1]:
            print(res[1].display_err(inp), file=sys.stderr)
        elif res[0]:
            print(res[0])

def set_setting(setting, value):
    settings[setting] = value

def save_settings():
    with open("./repl_settings.json", "w") as file:
        file.write(json.dumps(settings, indent=4))

def run_command(cmd):
    if cmd == "$!help":
        print("Commands")
        print("$!help - shows you all repl commands")
        print("$!setsetting - used to set an repl setting")
        print("$!savesettings - used to set the repl settings to a file")
        print("$!lssettings - used to get all setting keys")
        print("$!getsettings - used to get all setting key/value pairs")
        print("$!exit - exits the repl")
    elif cmd == "$!setsetting":
        print("Changing a setting, press enter to go back")
        setting_name = input("Name: ")
        if not setting_name: return
        new_val = input("Value (JSON): ")
        settings[setting_name] = json.loads(new_val) if new_val else ""
        print("Set successfully")
    elif cmd == "$!savesettings":
        save_settings()
        print("Saved successfully")
    elif cmd == "$!lssettings":
        print(", ".join([i for i in settings]))
    elif cmd == "$!getsettings":
        print(json.dumps(settings))
    elif cmd == "$!exit":
        return ("EXIT")
    else:
        print("Invalid command, see $!help for commands")
