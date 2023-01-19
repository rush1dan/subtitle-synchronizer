def modify_sub_files(files: list[str]):
    for file_path in files:
        lines = []
        with open(file_path) as file:
            lines = file.readlines()
            for line in lines:
                if "-->" in line:
                    print(line)