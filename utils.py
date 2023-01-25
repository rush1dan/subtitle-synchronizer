import re
from data import Data
from enum import IntEnum
import os
from tkinter import messagebox

class Duration_Unit(IntEnum):
    ms = 0
    s = 1
    m = 2
    h = 3

def process_dnd_data(data: str):
    braced_paths = get_braced_paths(data)
    non_braced_paths_string = data
    for braced_path in braced_paths:
        non_braced_paths_string = non_braced_paths_string.replace(braced_path, "")

    non_braced_paths_list = non_braced_paths_string.split()

    braces_stripped_paths_list = remove_braces_from_paths(braced_paths=braced_paths)

    all_files = []
    all_files.extend(non_braced_paths_list)
    all_files.extend(braces_stripped_paths_list)
    
    operable_files = []
    for file in all_files:
        file_ext = get_file_extension(file)
        if file_ext == ".srt" or file_ext == ".txt":
            operable_files.append(file)

    if len(operable_files) > 0:
        Data.set_data(operable_files)
    else:
        messagebox.showinfo(title="File Selection", message="Only .txt or .srt files allowed")

def get_braced_paths(data: str) -> list[str]:
    paths_surrounded_by_braces = re.findall(r'\{.*?\}', data)
    return paths_surrounded_by_braces

def remove_braces_from_paths(braced_paths: list[str]) -> list[str]:
    braceless_paths = [path.strip(r"{}") for path in braced_paths]
    return braceless_paths

def get_file_name(filepath: str, with_extension: bool = True):
    filename_rev = ""
    for i in range(len(filepath) - 1, -1, -1):
        ch = filepath[i]
        if ch == "/" or ch == "\\":
            break
        filename_rev += ch

        filename = filename_rev[::-1]
    return filename if with_extension else filename.replace(get_file_extension(filename), "")

def get_file_extension(filename_or_path: str):
    extension_rev = ""
    for i in range(len(filename_or_path) - 1, -1, -1):
        ch = filename_or_path[i]
        extension_rev += ch
        if ch == ".":
            break
    return extension_rev[::-1]

def get_parent_directory(file_or_folder_path: str) -> str:
    return os.path.dirname(os.path.realpath(file_or_folder_path))

def add_nonduplicate_identifier(filename_or_path: str, nonduplicate_identifier: str)->str:
    file_extension = get_file_extension(filename_or_path)
    modified_filename_or_path = filename_or_path.replace(file_extension, f"{nonduplicate_identifier}{file_extension}")
    if os.path.exists(modified_filename_or_path):
        modified_filename_or_path = add_nonduplicate_identifier(modified_filename_or_path, nonduplicate_identifier)
    return modified_filename_or_path

def center_window(width: int, height: int, screen_width: int, screen_height: int) -> str:
    # calculate position x and y coordinates
    x = int((screen_width/2)) - int((width/2))
    y = int((screen_height/2)) - int((height/2))
    return f'{width}x{height}+{x}+{y}'