import src.main as main
import EasyPart
import sys
import os
import datetime


def run():
    abs_path = os.path.abspath(__file__)[:-19]
    commands = {'exit', 'help', 'ls', 'cd', 'cat', 'cp', 'mv', 'rm'}

    print(abs_path+'\\ ', end='')


    for user_input in sys.stdin:
        user_input = user_input.split()
        user_command = user_input.pop(0)

        shell = open('shell.log', 'a')

        match user_command:
            case "help":
                print(commands)
                print(f"[{str(datetime.datetime.now())[:-7]}] {user_command} {user_input}", file=shell)

            case "exit":
                print(f"[{str(datetime.datetime.now())[:-7]}] {user_command} {user_input}", file=shell)
                break

            case "ls":
                ans = EasyPart.ls(abs_path, user_input)
                print(ans)
                if ans == None:
                    print(f"[{str(datetime.datetime.now())[:-7]}] {user_command} {user_input}", file=shell)
                else:
                    print(f"[{str(datetime.datetime.now())[:-7]}] {ans}", file=shell)

            case "cd":
                ans, abs_path = EasyPart.cd(abs_path, user_input)
                if ans == None:
                    print(f"[{str(datetime.datetime.now())[:-7]}] {user_command} {user_input}", file=shell)
                else:
                    print(ans)
                    print(f"[{str(datetime.datetime.now())[:-7]}] {ans}", file=shell)

            case "cat":
                ans = EasyPart.cat(abs_path, user_input)
                if ans == None:
                    print(f"[{str(datetime.datetime.now())[:-7]}] {user_command} {user_input}", file=shell)
                else:
                    print(ans)
                    print(f"[{str(datetime.datetime.now())[:-7]}] {ans}", file=shell)

            case 'cp':
                ans = EasyPart.cp(abs_path, user_input)
                if ans == None:
                    print(f"[{str(datetime.datetime.now())[:-7]}] {user_command} {user_input}", file=shell)
                else:
                    print(ans)
                    print(f"[{str(datetime.datetime.now())[:-7]}] {ans}", file=shell)

            case 'mv':
                ans = EasyPart.mv(abs_path, user_input)
                if ans == None:
                    print(f"[{str(datetime.datetime.now())[:-7]}] {user_command} {user_input}", file=shell)
                else:
                    print(ans)
                    print(f"[{str(datetime.datetime.now())[:-7]}] {ans}", file=shell)

            case 'rm':
                ans = EasyPart.rm(abs_path, user_input)
                if ans == None:
                    print(f"[{str(datetime.datetime.now())[:-7]}] {user_command} {user_input}", file=shell)
                else:
                    print(ans)
                    print(f"[{str(datetime.datetime.now())[:-7]}] {ans}", file=shell)

            case _:
                print("ERROR: Unknown command")
                print(f"[{str(datetime.datetime.now())[:-7]}] ERROR: Unknown command")


        abs_path = os.path.normpath(abs_path)
        print(abs_path, end=' ')


if __name__ == "__main__":
    main.main()