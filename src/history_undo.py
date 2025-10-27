import src.main as main
import os
import shutil


def history():
    try:
        his_file = open('his.history', 'r', encoding='utf-8')
        lines = [line[:-1] for line in his_file.readlines()]
        for num_line in range(len(lines)):
            print(f"{num_line + 1}: {lines[num_line]}")
        his_file.close()
        return None
    except:
        return "ERROR: Unknown error"


def undo():
    try:
        undo_file = open('undo_his.history', 'r', encoding='utf-8')
        lines = [line for line in undo_file.readlines()]
        undo_file.close()

        if len(lines) == 0:
            return 'ERROR: History of the undo is empty'
        else:
            new_undo_file = open('undo_his.history', 'w', encoding='utf-8')
            for line in lines[:-1]:
                new_undo_file.write(line)
            new_undo_file.close()
            abs_path, undo_command, undo_input = lines[-1].split(' <:> ')
            undo_input = undo_input.replace('\n', '')

            match undo_command:
                case 'rm':
                    operation = undo_input[0:2] if undo_input[0] == '-' else None
                    user_input = undo_input[3:] if operation else undo_input
                    file_path = user_input if user_input[1:2] == ':' else abs_path + '\\' + user_input
                    trash_path = f'{os.path.abspath(__file__)[:-19]}trash\\{file_path.split('\\')[-1]}'

                    os.replace(trash_path, file_path)

                case 'mv':
                    if '"' in undo_input:
                        file_path, new_path = undo_input.replace('" ', '"').split('"')[1:]
                    else:
                        file_path, new_path = undo_input.split(' ')
                    file_path = file_path if file_path[1:2] == ':' else abs_path + '\\' + file_path
                    new_path = new_path if new_path[1:2] == ':' else abs_path + '\\' + new_path

                    os.replace(new_path, file_path)

                case 'cp':
                    operation = undo_input[0:2] if undo_input[0] == '-' else None
                    user_input = undo_input[3:] if operation else undo_input

                    if '"' in user_input:
                        file_path, new_path = user_input.replace('" ', '"').split('"')[1:]
                    else:
                        file_path, new_path = user_input.split(' ')

                    new_path = new_path if new_path[1:2] == ':' else abs_path + '\\' + new_path
                    new_path += '\\' + file_path.split('\\')[-1]
                    if operation == '-r':
                        shutil.rmtree(new_path)
                    else:
                        os.remove(new_path)

                case _:
                    return "ERROR: Unknown command  in undo file"
    except:
        return "ERROR: Unknown error"


if __name__ == "__main__":
    main.main()