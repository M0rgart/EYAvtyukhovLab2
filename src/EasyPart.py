import os
from datetime import datetime
import shutil
import src.main as main


def ls(abs_path, user_input):
    '''Вывод содержимого директории. Если указан -l, то вывод более подробен. Доступен вызов без аргументов, по
    абсолютному и относительному пути'''
    try:
        #для ввода без аргументов
        if user_input == []:
            directory = os.listdir(abs_path)
            operation = None
        #разделение пути и оператора
        else:
            operation = user_input.pop(0) if user_input[0][0] == '-' else None
            path = ' '.join(user_input) if user_input else abs_path

            if path[1:3] != ':\\':
                path = abs_path + '\\' + path
            directory = os.listdir(path)
        #Подробный вывод при наличии -l
        if operation == '-l':
            for file in directory:
                file_info = (f"Name: {file:30}  Size:{int(os.path.getsize(path + "\\" + file)) // 8:12}  Date: "
                             f"{datetime.fromtimestamp(int(os.path.getatime(path + "\\" + file)))}  Permission: ")
                #Преобразование кода доступа в более привычный (алфавит: rwx-)
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
            return None
        #При отсутствии оператора
        elif operation == None:
            for file in directory:
                print(f"{file}")
            return None
        else:
            return "ERROR: Unknown operation"
    except (PermissionError):
        return "ERROR: Permission error"
    except (FileNotFoundError):
        return "ERROR: File not found"
    except (OSError):
        return "ERROR: OS error (try 'ls C:\\')"
    except Exception as e:
        return f"ERROR: {e}"


def cd(abs_path, user_input):
    '''Функция изменения пути. Способна принять как аргумент: абсолютный и относительный путь, а также
    (..) - переод на уровень выше и (~) - переход в домашний каталог'''
    old_path = abs_path #запоминаем старый путь, чтобы вернуть его при ошибке
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

    if os.path.isdir(abs_path):
        return None, abs_path + '\\'
    elif os.path.isfile(abs_path):
        return "ERROR: it is not directory", abs_path
    else:
        return "ERROR: File or directory does not exist", old_path


def cat(abs_path, user_input):
    '''Выводит содержимое файлов'''
    try:
        # Обрабатывает ввод, превращает в абсолютный путь к файлу
        user_input = ' '.join(user_input)
        if user_input[1:2] == ':':
            abs_path = user_input
        else:
            abs_path = abs_path + "\\" + user_input
        # Открывает файл по абсолютному пути, читает его построчно
        file = open(abs_path, 'r', encoding='utf-8')
        lines = [line[:-1] for line in file.readlines()]
        for num_line in range(len(lines)):
            print(f"{num_line+1}: {lines[num_line]}")
        file.close()
        return None
    except (FileNotFoundError):
        return "ERROR: File not found"
    except (PermissionError):
        return "ERROR: Permission error"
    except (UnicodeDecodeError):
        return "ERROR: Unicode decode error"
    except Exception as e:
        return f"ERROR: {e}"


def cp(abs_path, user_input):
    ''' Копирует файл или директорию. Поддерживается -r для рекурсивного копирования директорий.
    На ввод принимает как относительный, так и абсолютный путь. (.) - тоже работает '''
    try:
        # Выделение опреатора (если есть)
        user_input = ' '.join(user_input)
        operation = user_input[0:2] if user_input[0] == '-' else None
        user_input = user_input[3:] if operation else user_input
        # разделение ввода на путь к копируемому объекту и путь директории куда копировать
        if '"' in user_input:
            file_path, new_path = user_input.replace('" ', '"').split('"')[1:]
        else:
            file_path, new_path = user_input.split(' ')
        # приходим к абсолютному пути
        file_path = file_path if file_path[1:2] == ':' else abs_path + '\\' + file_path
        new_path = new_path if new_path[1:2] == ':' else abs_path + '\\' + new_path
        # Если есть оператор, то copytree, иначе copy
        if operation == None:
            shutil.copy(file_path, new_path)
            return None
        elif operation == '-r':
            shutil.copytree(file_path, new_path, dirs_exist_ok=True)
            return None
        else:
            return "ERROR: Unknown operation"
    except (PermissionError):
        return "ERROR: Permission error or add '-r'"
    except (FileNotFoundError):
        return "ERROR: File not found"
    except (ValueError):
        return "ERROR: Wrong number of arguments"
    except (shutil.Error):
        return "ERROR: Shutil error"
    except Exception as e:
        return f"ERROR: {e}"


def mv(abs_path, user_input):
    '''Перемещает файл на из одной директории в другую (работает с директориями, поддерживается .)'''
    try:
        # стандартная обработка :(
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
        # стандартная обработка закончилась :)
        os.replace(file_path, new_path) #перемещает файл\директорию в новое место
        return None

    except (FileNotFoundError):
        return "ERROR: File not found"
    except (PermissionError):
        return "ERROR: Permission error"
    except (ValueError):
        return "ERROR: Wrong number of arguments"
    except (os.error):
        return "ERROR: OSError"
    except Exception as e:
        return f"ERROR: {e}"


def rm(abs_path, user_input):
    '''Удаляет файл, при указании -r рекурсивно удалит директорию. На деле перемещает в директорию trash,
    тем самым можно откатить через undo.'''
    try:
        # обработка ввода
        user_input = ' '.join(user_input)
        operation = user_input[0:2] if user_input[0] == '-' else None
        user_input = user_input[3:] if operation else user_input

        file_path = user_input if user_input[1:2] == ':' else abs_path + '\\' + user_input
        #если есть -r работаем с директорией, если нет, то с файлом
        if operation == None and os.path.isfile(file_path) == 1:
            os.replace(file_path, f'{os.path.abspath(__file__)[:-15]}trash\\{file_path.split('\\')[-1]}')
            return None
        else:
            if operation == '-r':
                print(f"Delete the {file_path}? y/n")
                if input() == 'y':
                    os.replace(file_path, f'{os.path.abspath(__file__)[:-15]}trash\\{file_path.split('\\')[-1]}')
                    print(f'{file_path} deleted')
                    return None
                else:
                    print(f'{file_path} not deleted')
                    return None
            else:
                return "ERROR: Unknown operation or missing '-r'"
    except (PermissionError):
        return "ERROR: Permission error"
    except (FileNotFoundError):
        return "ERROR: File not found"
    except (ValueError):
        return "ERROR: Wrong number of arguments"
    except (IndexError):
        return "ERROR: Wrong number of arguments"
    except (OSError):
        return "ERROR: OSError"
    except (shutil.Error):
        return "ERROR: Shutil error"
    except Exception as e:
        return f"ERROR: {e}"


if __name__ == "__main__":
    main.main()