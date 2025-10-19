import sys
import os
from commandList import commands
from EasyPart import ls


def main() -> None:
    print("Для завершения ввода напишите exit")
    print("Чтобы увидеть список команд напишите help")
    abs_path = os.path.abspath(__file__)[:-12]
    for user_input in sys.stdin:
        user_input = user_input.split()
        user_command = user_input.pop(0)
        if user_command not in commands:
            exit("Unknown command")

        if user_command == "exit":
            break
        elif user_command == "help":
            print(commands)
        elif user_command == "ls":
            ls(abs_path, user_input)



if __name__ == "__main__":
    main()
