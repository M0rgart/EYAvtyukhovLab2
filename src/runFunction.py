import src.main as main
import EasyPart, zip_tar
import sys
import os
import logging


def run():
    abs_path = os.path.abspath(__file__)[:-19]
    commands = {'exit', 'help', 'ls', 'cd', 'cat', 'cp', 'mv', 'rm', 'zip', 'unzip'}

    print(abs_path+'\\ ', end='')


    for user_input in sys.stdin:
        if ' .\n' == user_input[-3:]:
            user_input = user_input[:-2] + abs_path

        user_input = user_input.split()
        user_command = user_input.pop(0)

        logging.basicConfig(level=logging.INFO, filename="shell.log", filemode="w",
                            format="%(asctime)s - %(levelname)s - %(message)s")


        match user_command:
            case "help":
                print(commands)
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


            case _:
                print("ERROR: Unknown command")
                ans = (f"ERROR: Unknown command")


        if not ans:
            logging.info(f"{user_command} {user_input}")
        else:
            print(ans)
            logging.error(ans)


        abs_path = os.path.normpath(abs_path)
        print(abs_path, end=' ')


if __name__ == "__main__":
    main.main()