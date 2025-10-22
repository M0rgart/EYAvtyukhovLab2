import os
from datetime import datetime
import shutil
import src.main as main


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
    except:
        print("Unexpected error")


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

def cat(abs_path, user_input):
    try:
        user_input = ' '.join(user_input)
        if user_input[1:2] == ':':
            abs_path = user_input
        else:
            abs_path = abs_path + "\\" + user_input
        file = open(abs_path, 'r', encoding='utf-8')
        lines = [line[:-1] for line in file.readlines()]
        for num_line in range(len(lines)):
            print(f"{num_line+1}: {lines[num_line]}")
        file.close()
    except (FileNotFoundError):
        print("File not found")
    except (PermissionError):
        print("Permission error")
    except (UnicodeDecodeError):
        print("Unicode decode error")
    except:
        print("Unexpected error")


def cp(abs_path, user_input):
    try:
        user_input = ' '.join(user_input)
        operation = user_input[0:2] if user_input[0] == '-' else None
        user_input = user_input[3:] if operation else user_input

        if '"' in user_input:
            file_path, new_path = user_input.replace('" ', '"').split('"')[1:]
        else:
            file_path, new_path = user_input.split(' ')

        file_path = file_path if file_path[1:2] == ':' else abs_path + '\\' + file_path
        new_path = new_path if new_path[1:2] == ':' else abs_path + '\\' + new_path

        if operation == None:
            shutil.copy2(file_path, new_path)
        elif operation == '-r':
            shutil.copytree(file_path, new_path, dirs_exist_ok=True)
        else:
            print("Unknown operation")
    except (PermissionError):
        print("Permission error or add '-r'")
    except (FileNotFoundError):
        print("File not found")
    except (ValueError):
        print("Wrong number of arguments")
    except (shutil.Error):
        print("Shutil error")


def mv(abs_path, user_input):
    try:
        user_input = ' '.join(user_input)

        if '"' in user_input:
            file_path, new_path = user_input.replace('" ', '"').split('"')[1:]
        else:
            file_path, new_path = user_input.split(' ')

        file_path = file_path if file_path[1:2] == ':' else abs_path + '\\' + file_path
        new_path = new_path if new_path[1:2] == ':' else abs_path + '\\' + new_path
        if '.' not in new_path:
            file_name = file_path.split('\\')[-1]
            new_path += '\\' + file_name

        os.replace(file_path, new_path)
    except (FileNotFoundError):
        print("File not found")
    except (PermissionError):
        print("Permission error")
    except (ValueError):
        print("Wrong number of arguments")
    except (os.error):
        print("OSError")
    except:
        print("Unexpected error")

def rm(abs_path, user_input):
    try:
        user_input = ' '.join(user_input)
        operation = user_input[0:2] if user_input[0] == '-' else None
        user_input = user_input[3:] if operation else user_input

        file_path = user_input if user_input[1:2] == ':' else abs_path + '\\' + user_input

        if operation == None:
            os.remove(file_path)
        else:
            if operation == '-r':
                print(f"Delete the {file_path}? y/n")
                if input() == 'y':
                    shutil.rmtree(file_path)
                    print(f'{file_path} deleted')
                else:
                    print(f'{file_path} not deleted')
            else:
                print("Unknown operation")
    except (PermissionError):
        print("Permission error")
    except (FileNotFoundError):
        print("File not found")
    except (ValueError):
        print("Wrong number of arguments")

if __name__ == "__main__":
    main.main()