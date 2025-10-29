import os.path
import re
import src.main as main


def find_in_file(path, pattern, regis):
    '''Функция для поиска в файле строк, которые совпадает с pattern. Сразу выводит название этого файла, номер строки
    и саму строку, если обнаружит совпадение'''
    try:
        f = open(path, 'r', encoding='utf-8')
        for line_num, line in enumerate(f, 1):
            if re.search(pattern, line, re.IGNORECASE) if regis else re.search(pattern, line):
                print(f'Name: {path.split('\\')[-1]:15} Number of line: {line_num:5} Line: {line.replace("\n", "")}')
    except PermissionError:
        return 'ERROR: PermissionError'
    except FileNotFoundError:
        return 'ERROR: FileNotFoundError'
    except Exception as e:
        return f"ERROR: {e}"


def grep(abs_path, user_input):
    '''Ищет все строк в файлах, совпадающие с указанным пользователем patten (всегда в кавычках).
    Поддерживает -r - рекурсивный поиск в каталогах и подкаталогах и -i - поиск без учета регистра'''
    try:
        # Определяет: рекурсивный поиск или нет \ учитывать регистр или нет
        recurs = True if '-r' in user_input else False
        regis = True if '-i' in user_input else False

        user_input = ' '.join(user_input)
        # Выделение патерна и абсолютного пути
        pattern = user_input[user_input.find('"')+1:user_input.rfind('"')]
        path = user_input[user_input.rfind('"')+2:]
        path = path if path[1:2] == ':' else abs_path + '\\' + path
        # Одиночный вызов функции для файла и многократный для каталогов (для всех файлов в нем и в его подкаталогах)
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
    except Exception as e:
        return f"ERROR: {e}"


if __name__ == "__main__":
    main.main()