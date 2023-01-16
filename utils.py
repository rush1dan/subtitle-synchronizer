import re
from data import Data

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

    Data.set_data(operable_files)

def get_braced_paths(data: str) -> list[str]:
    paths_surrounded_by_braces = re.findall(r'\{.*?\}', data)
    return paths_surrounded_by_braces

def remove_braces_from_paths(braced_paths: list[str]) -> list[str]:
    braceless_paths = [path.strip(r"{}") for path in braced_paths]
    return braceless_paths

def get_file_extension(filename_or_path: str):
    extension_rev = ""
    for i in range(len(filename_or_path) - 1, -1, -1):
        ch = filename_or_path[i]
        extension_rev += ch
        if ch == ".":
            break
    return extension_rev[::-1]