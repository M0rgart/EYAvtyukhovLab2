import src.main as main
import EasyPart
import sys
import os

def run():
    abs_path = os.path.abspath(__file__)[:-20]
    commands = {'exit', 'help', 'ls', 'cd', 'cat', 'cp', 'mv', 'rm'}

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
                EasyPart.ls(abs_path, user_input)

            case "cd":
                abs_path = EasyPart.cd(abs_path, user_input)

            case "cat":
                EasyPart.cat(abs_path, user_input)

            case 'cp':
                EasyPart.cp(abs_path, user_input)

            case 'mv':
                EasyPart.mv(abs_path, user_input)

            case 'rm':
                EasyPart.rm(abs_path, user_input)

            case _:
                print("Unknown command")


        abs_path = os.path.normpath(abs_path)
        print(abs_path, end=' ')


if __name__ == "__main__":
    main.main()
