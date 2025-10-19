import sys
import os
from commandList import commands
from EasyPart import ls, cd


def main() -> None:
    print("Для завершения ввода напишите exit")
    print("Чтобы увидеть список команд напишите help")

    abs_path = os.path.abspath(__file__)[:-12]
    print(abs_path+'\\ ', end='')
    for user_input in sys.stdin:
        user_input = user_input.split()
        user_command = user_input.pop(0)

        match user_command:
            case "help":
                print(commands)

            case "exit":
                break

            case "ls":
                ls(abs_path, user_input)

            case "cd":
                abs_path = cd(abs_path, user_input)

            case _:
                exit("Unknown command")


        if os.path.exists(abs_path):
            print(abs_path, end=' ')
        else:
            exit("File or directory does not exist")


if __name__ == "__main__":
    main()
