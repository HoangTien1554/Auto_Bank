import os
import psutil

def find_process(name):
    matches = []
    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            if proc.info['name'] and name.lower() in proc.info['name'].lower():
                matches.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return matches

def find_file(filename, search_root="C:\\"):
    for root, dirs, files in os.walk(search_root):
        if os.path.basename(root).lower() == "cagclick":
            # Bắt đầu tìm file bên trong CAGClick
            for subroot, subdirs, subfiles in os.walk(root):
                for file in subfiles:
                    if file.lower() == filename.lower():
                        return True
            return False
    return False

def check_app_active():
    if(find_process("CAG.exe") and find_file("CAG.exe") and find_file("CAG.pdb")):
        return True
    else:
        return False

