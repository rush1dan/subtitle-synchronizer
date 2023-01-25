from utils import Duration_Unit, add_nonduplicate_identifier, get_file_name

def modify_sub_files(files: list[str], duration: int, time_unit: Duration_Unit, save_directory: str):
    symbol = "-->"
    for file_path in files:
        file_r = open(file_path, "r")
        lines = file_r.readlines()
        line_count = len(lines)
        for i in range(0, line_count):
            if symbol in lines[i]:
                modify_line(i, lines, symbol, duration, time_unit)

        save_path = save_directory + "\\" + get_file_name(file_path)
        save_path = add_nonduplicate_identifier(save_path, "_Edited")

        file_w = open(save_path, "w")
        file_w.writelines(lines)
        
        file_r.close()
        file_w.flush()
        file_w.close()

def modify_line(line_index: int, lines: list[str], symbol: str, duration: int, time_unit: Duration_Unit):
    line = lines[line_index]
    timestamps = line.split(symbol)
    timestamps = [timestamp.strip(r" \n") for timestamp in timestamps]

    modified_timestamps = []
    for timestamp in timestamps:
        modified_timestamps.append(change_timestamp(timestamp, duration, time_unit))

    lines[line_index] = f"{modified_timestamps[0]} {symbol} {modified_timestamps[1]}\n"


def change_timestamp(timestamp: str, duration: int, time_unit: Duration_Unit) -> str:
    parts = timestamp.split(",")
    milliseconds = int(parts[1])

    first_parts = parts[0].split(":")
    seconds = int(first_parts[2])
    minutes = int(first_parts[1])
    hours = int(first_parts[0])

    total_milliseconds = (hours * 3600 + minutes * 60 + seconds) * 1000 + milliseconds

    total_milliseconds += convert_change_to_milliseconds(duration, time_unit)

    return deconvert_to_timestamp(total_milliseconds)


def convert_change_to_milliseconds(duration: int, time_unit: Duration_Unit) -> int:
    match(time_unit):
        case Duration_Unit.ms:
            return duration
        case Duration_Unit.s:
            return duration * 1000
        case Duration_Unit.m:
            return duration * 60 * 1000
        case Duration_Unit.h:
            return duration * 3600 * 1000
        case _:
            print("Unrecognized time unit.")

def deconvert_to_timestamp(total_milliseconds: int) -> str:
    seconds = total_milliseconds // 1000
    milliseconds = total_milliseconds % 1000
    minutes = seconds // 60
    seconds = seconds % 60
    hours = minutes // 60
    minutes = minutes % 60

    return f"{str(hours).zfill(2)}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)},{str(milliseconds).zfill(3)}"





