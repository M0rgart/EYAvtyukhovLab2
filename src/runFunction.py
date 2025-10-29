from sqlalchemy.cyextension.immutabledict import immutabledict

import src.main as main
import src.EasyPart as EasyPart
import src.zip_tar as zip_tar
import src.grep as grep
import src.history_undo as history_undo
import src.help as help
import sys, os, shutil
import logging


def run():
    '''Основная функция. При ее вызове:
    1) Очищается история undo и директория trash
    2) Запускается непрерывный ввод со стороны пользователя (sys.stdin)
    3) Из введеных данных выделяется команда, затем через match вызывается соответствующая функция
    4) Если функция возвращет None => она сделала все павильно. Заполняется история, логи, история undo если
    команда rm, mv или cp. Иначе функции возвращают ошибку, которая записывается в логи.
    5) В конце выводит абсолютный путь в котором сейчас находится пользователь'''
    with open('undo_his.history', 'w', encoding='utf-8') as f:
        f.close()
    abs_path = os.path.abspath(__file__)[:-19]

    trash = abs_path+'\\trash' #абсолютный путь к директории\мусорки

    #Удаление всех файлов в каталоге trash
    for file_name in os.listdir(trash):
        path = os.path.join(trash, file_name)
        try:
            if os.path.isfile(path) or os.path.islink(path):
                os.unlink(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
        except Exception:
            print(f'Failed to delete {file_name}. Reason: {Exception}')

    print(abs_path+'\\ ', end='')

    #Непрерывный ввод
    for user_input in sys.stdin:
        if ' .\n' == user_input[-3:]:
            user_input = user_input[:-2] + abs_path
            print(user_input)

        #Разделение ввода на команду и переменные
        user_input = user_input.split()
        user_command = user_input.pop(0)

        #Логи
        logging.basicConfig(level=logging.INFO, filename="shell.log", filemode="w",
                            format="%(asctime)s - %(levelname)s - %(message)s")

        #Вызов функций соответствующих введеным пользователеи команд
        match user_command:
            case "help":
                help.help(user_input)
                ans = None

            case "exit":
                logging.info(f"{user_command} {user_input}")
                break

            case "ls":
                ans = EasyPart.ls(abs_path, user_input)


            case "cd":
                ans, abs_path = EasyPart.cd(abs_path, user_input)


            case "cat":
                ans = EasyPart.cat(abs_path, user_input)


            case 'cp':
                ans = EasyPart.cp(abs_path, user_input)


            case 'mv':
                ans = EasyPart.mv(abs_path, user_input)


            case 'rm':
                ans = EasyPart.rm(abs_path, user_input)


            case 'zip':
                ans = zip_tar.zip(abs_path, user_input)


            case 'unzip':
                ans = zip_tar.unzip(abs_path, user_input)


            case 'tar':
                ans = zip_tar.tar(abs_path, user_input)


            case 'untar':
                ans = zip_tar.untar(abs_path, user_input)


            case 'grep':
                ans = grep.grep(abs_path, user_input)


            case 'history':
                ans = history_undo.history()


            case 'undo':
                ans = history_undo.undo()


            case _:
                ans = (f"ERROR: Unknown command")

        #Если функция завершилась успешно
        if not ans:
            logging.info(f"{user_command} {user_input}") # запись в логи

            his_file = open('his.history', 'r', encoding='utf-8') # запись в историю
            lines = [line[:-1] for line in his_file.readlines()]
            his_file.close()
            new_his_file = open('his.history', 'w', encoding='utf-8')

            if len(lines) >= 10:
                lines = lines[1:10]
            for line in lines:
                new_his_file.write(line + '\n')
            new_his_file.write(f"{user_command} {' '.join(user_input)}\n")
            new_his_file.close()

            if user_command in ['mv', 'rm', 'cp']: # запись в историю undo
                undo_his_file = open('undo_his.history', 'r', encoding='utf-8')
                lines = [line[:-1] for line in undo_his_file.readlines()]
                undo_his_file.close()
                new_undo_his_file = open('undo_his.history', 'w', encoding='utf-8')

                if len(lines) >= 3:
                    deleted = lines[0:1][0].split(' <:> ')
                    lines = lines[1:3]
                    if deleted[1] == 'rm':
                        del_path = trash + '\\' + deleted[2].split('\\')[-1].replace('-r ', '')
                        if os.path.isfile(del_path):
                            os.remove(del_path)
                        else:
                            shutil.rmtree(del_path)
                for line in lines:
                    new_undo_his_file.write(line + '\n')
                new_undo_his_file.write(f"{abs_path} <:> {user_command} <:> {' '.join(user_input)}\n")
                new_undo_his_file.close()

        # Функция завершилась с ошибкой => вывод пользователю и запись в логи с уровнем ERROR
        else:
            print(ans)
            logging.error(ans)

        # нормализация и вывод абсолютного пути директории, в которой находится пользователь
        abs_path = os.path.normpath(abs_path)
        print(abs_path, end=' ')


if __name__ == "__main__":
    main.main()