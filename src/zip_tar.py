import zipfile
import tarfile
import shutil



def zip(abs_path, user_input):
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
    except:
        return "ERROR: Unexpected error"