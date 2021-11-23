# encoding: utf-8

# library
import sys
import time
import platform
from tabulate import tabulate

# import custom module
from mymodule.drive import quickstart
from mymodule.drive.DriveFile import DriveFile


def cmd_list():
    list_commands = '''
          [ login - login to google drive ] [ exit ]
               
    ls   - list directory            mkdir - make directory
    rm   - remove file/directory     get   - download file
    com  - list commands             put   - upload file
    link - view file (link)          mv    - move file     
    '''
    return list_commands


def ls_command(cmd):
    path = cmd[1] if len(cmd) != 1 else 'root'
    try:
        ls = DriveFile('credentials_module.json').searchFile(f"'{path}' in parents and trashed=false")
        dataFile = {
            'name': [i['title'] for i in ls],
            #'size': [i['size'] for i in ls],
            'id': [i['id'] for i in ls]
        }
        table = tabulate(dataFile, headers=['name', 'id'], showindex=True)
        return table
    except:
        return 'error'


def mkdir_command(cmd):
    if len(cmd) != 2 and len(cmd) != 3:
        return 'mkdir: missing operand. mkdir <folder_id> <name>'
    try:
        folder_id = cmd[1] if len(cmd) != 2 else 'root'
        path = cmd[2] if len(cmd) != 2 else cmd[1]
        DriveFile('credentials_module.json').createFolder(folder_id, path)
        return f'mkdir success crete folder [{path}]'
    except:
        return f'error create file'


def rm_command(cmd):
    if len(cmd) != 2 and len(cmd) != 3:
        return 'rm: missing operand. rm <mode> <file_id>'
    try:
        mode = 'permanent' if str(cmd[1]) == '-p' else 'trash'
        mode = 'outTrash' if str(cmd[1]) == '-outTrash' else mode
        id_file = cmd[2] if len(cmd) != 2 else cmd[1]
        DriveFile('credentials_module.json').removeFile(id_file, mode)
        return f'rm success remove file [{id_file}]'
    except:
        return f'error remove'


def get_command(cmd):
    if len(cmd) != 2 and len(cmd) != 3:
        return 'get: missing operand. get <id_file> <path>'
    try:
        id_file = cmd[1]
        path = cmd[2] if len(cmd) != 2 else '.{slash}'.format(slash=slash_system)
        path = path.replace('#', ' ')
        name_file = DriveFile('credentials_module.json').downloadFile(id_file, path)
        return f'download success file [{name_file}]'
    except:
        return f'error download [{cmd[1]}]'


def put_command(cmd):
    if len(cmd) != 2 and len(cmd) != 3:
        return 'put: missing operand. put <id_folder> <path>'
    try:
        id_folder = cmd[1] if len(cmd) != 2 else 'root'
        path = cmd[2] if len(cmd) != 2 else cmd[1]
        path = path.replace('#', ' ')
        name_file = DriveFile('credentials_module.json').uploadFile(id_folder, path)
        return f'upload success, file [{name_file}]'
    except:
        return f'error upload'


def link_command(cmd):
    path = cmd[1] if len(cmd) != 1 else 'root'
    try:
        ls = DriveFile('credentials_module.json').searchFile(f"'{path}' in parents and trashed=false")
        dataFile = {
            'name': [i['title'] for i in ls],
            #'id': [i['id'] for i in ls],
            'link': [i['link'] for i in ls]
        }
        table = tabulate(dataFile, headers=['name', 'link'], showindex=True)
        return table
    except:
        return 'error'


def commands(cmd):
    command = cmd[0]
    if command == 'login':
        quickstart.login()
        return 'login success'
    elif command == 'exit':
        sys.exit(0)
    elif command == 'ls':
        return ls_command(cmd)
    elif command == 'com':
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
    else:
        return 'Command not found'


def main():
    global slash_system
    slash_system = '\\' if platform.system().lower() == 'windows' else '/'
    cmd = input('> ')
    cmd = cmd.split(' ')
    out_command = commands(cmd)
    print(out_command)


print(cmd_list())
while True:
    try:
        main()
        time.sleep(0.5)
    except Exception as e:
        print(f'ERROR:\n{e}')