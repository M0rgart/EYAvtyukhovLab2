import src.main as main
import shutil



def zip(abs_path, user_input):
    '''Создает из файла или каталога zip-архив'''
    try:
        user_input = ' '.join(user_input)

        if '"' in user_input:
            file_path, file_name = user_input.replace('" ', '"').split('"')[1:]
        else:
            file_path, file_name = user_input.split(' ')

        file_path = file_path if file_path[1:2] == ':' else abs_path + '\\' + file_path
        file_name = file_name.replace('.zip', '')

        shutil.make_archive(file_name, 'zip', file_path)
        return None
    except (shutil.Error):
        return "ERROR: Shutil error"
    except (PermissionError):
        return "ERROR: Permission error"
    except (FileNotFoundError):
        return "ERROR: File not found"
    except (ValueError):
        return "ERROR: Wrong number of arguments"
    except (IndexError):
        return "ERROR: Wrong number of arguments"
    except Exception as e:
        return f"ERROR: {e}"


def unzip(abs_path, user_input):
    '''Распаковывает zip-архив'''
    try:
        if user_input == []:
            return "ERROR: Wrong number of arguments"
        user_input = ' '.join(user_input)

        file_path = user_input if user_input[1:2] == ':' else abs_path + '\\' + user_input

        if file_path.endswith('.zip') == 0:
            file_path = file_path + '.zip'

        shutil.unpack_archive(file_path)
        return None

    except (shutil.Error):
        return "ERROR: Shutil error"
    except (shutil.ReadError):
        return "ERROR: It is not zip file"
    except (PermissionError):
        return "ERROR: Permission error"
    except (FileNotFoundError):
        return "ERROR: File not found"
    except (ValueError):
        return "ERROR: Wrong number of arguments"
    except (IndexError):
        return "ERROR: Wrong number of arguments"
    except Exception as e:
        return f"ERROR: {e}"


def tar(abs_path, user_input):
    '''Создает из файла или каталога tar-архив'''
    try:
        user_input = ' '.join(user_input)

        if '"' in user_input:
            file_path, file_name = user_input.replace('" ', '"').split('"')[1:]
        else:
            file_path, file_name = user_input.split(' ')

        file_path = file_path if file_path[1:2] == ':' else abs_path + '\\' + file_path
        file_name = file_name.replace('.tar', '')

        shutil.make_archive(file_name, 'gztar', file_path)
        return None
    except (shutil.Error):
        return "ERROR: Shutil error"
    except (PermissionError):
        return "ERROR: Permission error"
    except (FileNotFoundError):
        return "ERROR: File not found"
    except (ValueError):
        return "ERROR: Wrong number of arguments"
    except (IndexError):
        return "ERROR: Wrong number of arguments"
    except Exception as e:
        return f"ERROR: {e}"


def untar(abs_path, user_input):
    '''Распаковывает tar-архив'''
    try:
        if user_input == []:
            return "ERROR: Wrong number of arguments"
        user_input = ' '.join(user_input)

        file_path = user_input if user_input[1:2] == ':' else abs_path + '\\' + user_input

        if file_path.endswith('.tar.gz') == 0:
            file_path = file_path + '.tar.gz'

        shutil.unpack_archive(file_path)
        return None

    except (shutil.Error):
        return "ERROR: Shutil error"
    except (shutil.ReadError):
        return "ERROR: It is not zip file"
    except (PermissionError):
        return "ERROR: Permission error"
    except (FileNotFoundError):
        return "ERROR: File not found"
    except (ValueError):
        return "ERROR: Wrong number of arguments"
    except (IndexError):
        return "ERROR: Wrong number of arguments"
    except Exception as e:
        return f"ERROR: {e}"

if __name__ == "__main__":
    main.main()