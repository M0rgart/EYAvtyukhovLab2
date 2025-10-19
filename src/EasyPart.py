import os
from datetime import datetime


def ls(abs_path, user_input):
    try:
        path = user_input[-1] if user_input and user_input != ['-l'] else abs_path
        user_input = [0] if not user_input else user_input
        directory = []
        if path[1:3] != ':\\':
            path = abs_path + '\\' + path
        directory = os.listdir(path)

        if user_input[0] == '-l':
            for file in directory:
                file_info = (f"Name: {file:30}  Size:{int(os.path.getsize(path + "\\" + file))//8:12}  Date: "
                      f"{datetime.fromtimestamp(int(os.path.getctime(path + "\\" + file)))}  Permission: ")
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
        else:
            for file in directory:
                print(f"{file}")
    except:
        if len(user_input) <= 1:
            exit(f'The directory "{user_input}" does not exist.')
        else:
            exit(f'The directory "{user_input[1]}" does not exist or unknown option.')