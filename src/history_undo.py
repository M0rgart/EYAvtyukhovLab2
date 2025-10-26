import src.main as main


def history():
    his_file = open('his.history', 'r', encoding='utf-8')
    lines = [line[:-1] for line in his_file.readlines()]
    for num_line in range(len(lines)):
        print(f"{num_line + 1}: {lines[num_line]}")
    his_file.close()


def undo():
    pass


if __name__ == "__main__":
    main.main()