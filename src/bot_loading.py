import os
import sys
import importlib

BOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Bots"))

def _list_bot_scripts(folder_path):
    if not os.path.isdir(folder_path):
        return []
    modules = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".py") and filename != "EmptyBot.py":
            modules.append(os.path.splitext(filename)[0])
    return modules

def _import_modules_from_folder(folder_path, module_names):
    """
    Import each module by name from folder_path.
    Returns dict: {module_name: imported_module}
    """
    if folder_path not in sys.path:
        sys.path.insert(0, folder_path)

    imported = {}
    for name in module_names:
        try:
            imported[name] = importlib.import_module(name)
        except Exception as e:
            print(f"Failed to import {name}: {e}")
    return imported

def get_bots():
    return _import_modules_from_folder(BOT_DIR, _list_bot_scripts(BOT_DIR))
