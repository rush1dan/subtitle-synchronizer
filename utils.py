import re

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
    print(all_files)
    

def get_braced_paths(data: str) -> list[str]:
    paths_surrounded_by_braces = re.findall(r'\{.*?\}', data)
    return paths_surrounded_by_braces

def remove_braces_from_paths(braced_paths: list[str]) -> list[str]:
    braceless_paths = [path.strip(r"{}") for path in braced_paths]
    return braceless_paths