import os.path
import re
import src.main as main


def find_in_file(path, pattern, regis):
    try:
        f = open(path, 'r', encoding='utf-8')
        for line_num, line in enumerate(f, 1):
            if re.search(pattern, line, re.IGNORECASE) if regis else re.search(pattern, line):
                print(f'Name: {path.split('\\')[-1]:15} Number of line: {line_num:5} Line: {line.replace("\n", "")}')
    except PermissionError:
        return 'ERROR: PermissionError'
    except FileNotFoundError:
        return 'ERROR: FileNotFoundError'
    except Exception:
        return f"ERROR: {Exception}"


def grep(abs_path, user_input):
    try:
        recurs = True if '-r' in user_input else False
        regis = True if '-i' in user_input else False

        pattern = user_input[-2][1:-1]
        path = user_input[-1]
        path = path if path[1:2] == ':' else abs_path + '\\' + path

        if os.path.isfile(path):
            find_in_file(path, pattern, regis)
        elif os.path.isdir(path):
            if recurs:
                for root, _, files in os.walk(path):
                    for name in files:
                        find_in_file(os.path.join(root, name), pattern, regis)
            else:
                return "ERROR: missing -r"
        else:
            return f"ERROR: {path} is not a file or directory"
    except Exception:
        return f"ERROR: {Exception}"


if __name__ == "__main__":
    main.main()