import os
import shutil
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

def get_minecraft_folder(default_path):
    root = tk.Tk()
    root.withdraw()
    
    if messagebox.askyesno("Folder verification", f"Is this .minecraft folder correct for mods installation?\n\n{default_path}"):
        return default_path
    
    folder_path = filedialog.askdirectory(initialdir=default_path, title="Select .minecraft folder")
    return folder_path if folder_path else default_path

def install_files(minecraft_folder):
    if messagebox.askyesno("Confirmation", "Do you want to proceed with file installation?\n\nThis will delete the files in your mods folder to add new ones"):
        source_folder = resource_path('files_for_.minecraft_folder')
        
        for item in os.listdir(source_folder):
            s = os.path.join(source_folder, item)
            d = os.path.join(minecraft_folder, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)

        activate_resource_packs(minecraft_folder)
        
        messagebox.showinfo("Success", "Files were installed successfully!\n\nYou can delete this file and launch Minecraft in the correct version.")
    else:
        messagebox.showinfo("Cancelled", "Installation was cancelled.")

def activate_resource_packs(minecraft_folder):
    resourcepacks_folder = resource_path('files_for_.minecraft_folder/resourcepacks')
    resource_packs = sorted(os.listdir(resourcepacks_folder))
    cleaned_resource_packs = []
    for pack in resource_packs:
        cleaned_name = pack.replace('§', '_').replace(' ', '_')
        cleaned_resource_packs.append(cleaned_name)
    formatted_resource_packs = ','.join(f'"{pack}"' for pack in cleaned_resource_packs)
    options_file_path = os.path.join(minecraft_folder, 'options.txt')
    with open(options_file_path, 'r') as file:
        lines = file.readlines()
    for i in range(len(lines)):
        if lines[i].startswith('resourcePacks:'):
            lines[i] = f'resourcePacks:[{formatted_resource_packs}]\n'
            break
    with open(options_file_path, 'w') as file:
        file.writelines(lines)

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

if __name__ == '__main__':
    if not is_admin():
        run_as_admin()
    else:
        default_path = os.path.expandvars(r'%APPDATA%\.minecraft')
        minecraft_folder = get_minecraft_folder(default_path)
        install_files(minecraft_folder)
