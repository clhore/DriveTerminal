# encoding: utf-8

# library
import sys
import time
import os
import threading
from tabulate import tabulate

# import custom module
from mymodule.drive import quickstart
from mymodule.drive.DriveFile import DriveFile


def cmd_list():
    list_commands = '''
          [ login - login to google drive ] [ exit ]

    ls   - list directory            mkdir - make directory
    rm   - remove file/directory     get   - download file
    help - list commands             put   - upload file
    link - view file (link)          !     - local command
    '''
    return list_commands


def ls_command(cmd):
    cmd_split = cmd.split(' ')
    trash = 'true' if len(cmd_split) > 1 and cmd_split[1] == '-trash' else 'false'
    path = cmd_split[1] if len(cmd_split) == 2 and cmd_split[1] != '-trash' else 'root'
    path = cmd_split[2] if len(cmd_split) == 3 else path
    # print(f"'{path}' in parents and trashed={trash}")
    try:
        ls = DriveFile(credentials_module).searchFile(f"'{path}' in parents and trashed={trash}")
        dataFile = {
            'name': [i['title'] for i in ls],
            # 'size': [i['size'] for i in ls],
            'id': [i['id'] for i in ls]
        }
        table = tabulate(dataFile, headers=['name', 'id'], showindex=True)
        return table
    except:
        return 'ls: error'


def mkdir_command(cmd):
    cmd_split = cmd.split(' ')
    if len(cmd_split) != 2 and len(cmd_split) != 3:
        return 'mkdir: missing operand. mkdir <folder_id> <name>'
    try:
        folder_id = cmd_split[1] if len(cmd_split) != 2 else 'root'
        path = cmd_split[2] if len(cmd_split) != 2 else cmd_split[1]
        DriveFile(credentials_module).createFolder(folder_id, path)
        return f'mkdir success crete folder [{path}]'
    except:
        return f'error create file'


def rm_command(cmd):
    cmd_split = cmd.split(' ')
    if len(cmd_split) != 2 and len(cmd_split) != 3:
        return 'rm: missing operand. rm <mode> <file_id>'
    try:
        mode = 'permanent' if str(cmd_split[1]) == '-p' else 'trash'
        mode = 'outTrash' if str(cmd_split[1]) == '-outTrash' else mode
        string_IDs = cmd_split[2] if len(cmd_split) != 2 else cmd_split[1]
        list_IDs = string_IDs.split(',')
        list_thread = list()
        for id_file in list_IDs:
            thread = threading.Thread(target=DriveFile(credentials_module).removeFile, args=(id_file, mode))
            list_thread.append(thread)
            thread.start()
            # DriveFile(credentials_module).removeFile(id_file, mode)
        for thread in list_thread:
            thread.join()
        return f'rm success remove file {string_IDs}'
    except:
        return f'error remove'


def get_command(cmd):
    cmd_split = cmd.split(' ')
    if len(cmd_split) != 2 and len(cmd_split) != 3:
        return 'get: missing operand. get <id_file> <path>'
    try:
        string_IDs = cmd_split[1]
        list_IDs = string_IDs.split(',')
        path = cmd_split[2] if len(cmd_split) != 2 else './'
        path = path.replace('#', ' ')
        list_thread = list()
        for id_file in list_IDs:
            thread = threading.Thread(target=DriveFile(credentials_module).downloadFile, args=(id_file, path))
            list_thread.append(thread)
            thread.start()
            # DriveFile(credentials_module).downloadFile(id_file, path)
        for thread in list_thread:
            thread.join()
        return f'get: download success'
    except:
        return f'get: error download'


def put_command(cmd):
    cmd_split = cmd.split(' ')
    if len(cmd_split) != 2 and len(cmd_split) != 3:
        return 'put: missing operand. put <id_folder> <path>'
    try:
        id_folder = cmd_split[1] if len(cmd_split) != 2 else 'root'
        string_path = cmd_split[2] if len(cmd_split) != 2 else cmd_split[1]
        string_path = string_path.replace('#', ' ')
        list_path = string_path.split(',')
        list_thread = list()
        for path in list_path:
            thread = threading.Thread(target=DriveFile(credentials_module).uploadFile, args=(id_folder, path))
            list_thread.append(thread)
            thread.start()
            # DriveFile(credentials_module).uploadFile(id_folder, path)
        for thread in list_thread:
            thread.join()
        return f'put: upload success'
    except:
        return f'put: error upload'


def link_command(cmd):
    cmd_split = cmd.split(' ')
    path = cmd_split[1] if len(cmd_split) != 1 else 'root'
    try:
        ls = DriveFile(credentials_module).searchFile(f"'{path}' in parents and trashed=false")
        dataFile = {
            'name': [i['title'] for i in ls],
            # 'id': [i['id'] for i in ls],
            'link': [i['link'] for i in ls]
        }
        table = tabulate(dataFile, headers=['name', 'link'], showindex=True)
        return table
    except:
        return 'error'


def local_command(cmd):
    command = cmd.replace('!', '')
    try:
        os.system(command)
        return f'!: local command [{command}]'
    except:
        return '!: error local command'


def commands(cmd):
    command = cmd.split(' ')[0]
    if command == 'login':
        quickstart.login()
        return 'login success'
    elif command == 'exit':
        sys.exit(0)
    elif command == 'ls':
        return ls_command(cmd)
    elif command == 'help':
        return cmd_list()
    elif command == 'mkdir':
        return mkdir_command(cmd)
    elif command == 'rm':
        return rm_command(cmd)
    elif command == 'get':
        return get_command(cmd)
    elif command == 'put':
        return put_command(cmd)
    elif command == 'link':
        return link_command(cmd)
    elif str(command[0:1]) == '!':
        return local_command(cmd)
    else:
        return 'Invalid command'


def main():
    cmd = input('> ')
    out_command = commands(cmd)
    print(out_command)


if __name__ == '__main__':
    global credentials_module
    credentials_module = 'credentials_module.json'

    print(cmd_list())
    while True:
        try:
            main()
            time.sleep(0.1)
        except Exception as e:
            print(f'ERROR:\n{e}')