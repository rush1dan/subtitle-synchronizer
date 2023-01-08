import re

def process_dnd_data(data: str):
    braced_paths = get_braced_paths(data)
    non_braced_paths_string = data
    for braced_path in braced_paths:
        non_braced_paths_string = non_braced_paths_string.replace(braced_path, "")
        #bug: results in empty strings

    non_braced_paths_list = non_braced_paths_string.split(" ")
    print("non_braced_paths: \n")
    print(non_braced_paths_list)

    braces_stripped_paths_list = remore_braces_from_paths(braced_paths=braced_paths)
    print("\n braced_paths_stripped: \n")
    print(braces_stripped_paths_list)
    

def get_braced_paths(data: str) -> list[str]:
    paths_surrounded_by_braces = re.findall(r'\{.*?\}', data)
    return paths_surrounded_by_braces

def remore_braces_from_paths(braced_paths: list[str]) -> list[str]:
    braceless_paths = [path.strip(r"{}") for path in braced_paths]
    return braceless_paths