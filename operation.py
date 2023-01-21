from utils import Duration_Unit

def modify_sub_files(files: list[str], duration: int, time_unit: Duration_Unit):
    id_string = "-->"
    for file_path in files:
        lines = []
        with open(file_path) as file:
            lines = file.readlines()
            for line in lines:
                if id_string in line:
                    modify_line(line, id_string, duration, time_unit)


def modify_line(line: str, id_string: str, duration: int, time_unit: Duration_Unit):
    timestamps = line.split(id_string)
    timestamps = [timestamp.strip(r" \n") for timestamp in timestamps]

    for timestamp in timestamps:
        print(change_timestamp(timestamp, duration, time_unit))


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





