import os
from config_manager import load_config

def execute_transaction(content, amount):
    config = load_config()
    ahk_file = config["ahk_file"]
    ahk_run = os.path.normpath(os.path.join("ahk", ahk_file))

    with open(ahk_run, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if "TaiKhoan := " in line:
            lines[i] = f'TaiKhoan := "{content}"\n'
        if "SoTien := " in line:
            lines[i] = f"SoTien := {amount}\n"
            break

    with open(ahk_run, "w", encoding="utf-8") as file:
        file.writelines(lines)

    os.startfile(ahk_run)