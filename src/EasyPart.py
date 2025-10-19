import os
from datetime import datetime


def ls(abs_path, user_input):
    try:
        if user_input == []:
            directory = os.listdir(abs_path)
            operation = None
        else:
            operation = user_input.pop(0) if user_input[0][0] == '-' else None
            path = ' '.join(user_input) if user_input else abs_path

            if path[1:3] != ':\\':
                path = abs_path + '\\' + path
            directory = os.listdir(path)

        if operation == '-l':
            for file in directory:
                file_info = (f"Name: {file:30}  Size:{int(os.path.getsize(path + "\\" + file)) // 8:12}  Date: "
                             f"{datetime.fromtimestamp(int(os.path.getatime(path + "\\" + file)))}  Permission: ")
                file_permission = f"{bin(os.stat(path + "\\" + file).st_mode)[-12:]}"
                for i in range(len(file_permission)):
                    if file_permission[i] == '1':
                        if i % 3 == 0:
                            file_info += 'r'
                        elif i % 3 == 1:
                            file_info += 'w'
                        else:
                            file_info += 'x'
                    else:
                        file_info += '-'
                print(file_info)
        elif operation == None:
            for file in directory:
                print(f"{file}")
        else:
            print("Unknown operation")
    except (PermissionError):
        print("Permission error")
    except (FileNotFoundError):
        print("File not found")
    except (OSError):
        print("OS error (try 'ls C:\\')")


def cd(abs_path, user_input):
    old_path = abs_path
    if user_input == ['..']:
        abs_path = '\\'.join(abs_path.split('\\')[:-1])
    elif user_input == ['~']:
        abs_path = os.path.expanduser('~')
    else:
        user_input = ' '.join(user_input)
        if user_input[1:2] == ':':
            abs_path = user_input
        else:
            abs_path = abs_path + "\\" + user_input

    if os.path.exists(abs_path):
        return abs_path + '\\'
    else:
        print("File or directory does not exist")
        return old_path
