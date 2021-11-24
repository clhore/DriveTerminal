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
    path = cmd_split[1] if len(cmd_split) != 1 else 'root'
    try:
        ls = DriveFile('credentials_module.json').searchFile(f"'{path}' in parents and trashed=false")
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
        DriveFile('credentials_module.json').createFolder(folder_id, path)
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
        id_file = cmd_split[2] if len(cmd_split) != 2 else cmd_split[1]
        DriveFile('credentials_module.json').removeFile(id_file, mode)
        return f'rm success remove file {id_file}'
    except:
        return f'error remove'


def get_command(cmd):
    cmd_split = cmd.split(' ')
    if len(cmd_split) != 2 and len(cmd_split) != 3:
        return 'get: missing operand. get <id_file> <path>'
    try:
        id_file = cmd_split[1]
        path = cmd_split[2] if len(cmd_split) != 2 else './'
        path = path.replace('#', ' ')
        name_file = DriveFile('credentials_module.json').downloadFile(id_file, path)
        return f'download success file [{name_file}]'
    except:
        return f'error download'


def put_command(cmd):
    cmd_split = cmd.split(' ')
    if len(cmd_split) != 2 and len(cmd_split) != 3:
        return 'put: missing operand. put <id_folder> <path>'
    try:
        id_folder = cmd_split[1] if len(cmd_split) != 2 else 'root'
        path = cmd_split[2] if len(cmd_split) != 2 else cmd_split[1]
        path = path.replace('#', ' ')
        name_file = DriveFile('credentials_module.json').uploadFile(id_folder, path)
        return f'upload success, file [{name_file}]'
    except:
        return f'error upload'


def link_command(cmd):
    cmd_split = cmd.split(' ')
    path = cmd_split[1] if len(cmd_split) != 1 else 'root'
    try:
        ls = DriveFile('credentials_module.json').searchFile(f"'{path}' in parents and trashed=false")
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

    switcher = {
        'login': quickstart.login(),
        'help': cmd_list(),
        'ls': ls_command(cmd),
        'mkdir': mkdir_command(cmd),
        'rm': rm_command(cmd),
        'get': get_command(cmd),
        'put': put_command(cmd),
        'link': link_command(cmd),
    }
    return local_command(cmd) if cmd[0:1] == '!' else switcher.get(cmd.split(' ')[0], "Invalid command")

    '''
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
        return 'Command not found'
    '''


def main():
    cmd = input('> ')
    out_command = commands(cmd) if cmd != 'exit' else sys.exit(0)
    print(out_command)


print(cmd_list())
while True:
    try:
        main()
        time.sleep(0.1)
    except Exception as e:
        print(f'ERROR:\n{e}')
