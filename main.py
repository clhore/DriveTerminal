# encoding: utf-8

# library
import sys
import time
from tabulate import tabulate

# import custom module
from mymodule.drive import quickstart
from mymodule.drive.DriveFile import DriveFile


def cmd_list():
    list_commands = '''
          [ login - login to google drive ] [ exit ]
               
    ls  - list directory             mkdir - make directory
    rm  - remove file/directory      get   - download file
    com - list commands              put   - upload file     
    '''
    return list_commands


def ls_command(cmd):
    try:
        path = 'root'
        if len(cmd) != 1:
            path = cmd[1]
        ls = DriveFile('credentials_module.json').searchFile(f"'{path}' in parents and trashed=false")
        # print(ls)
        dataFile = {
            'name': [], 'id': []
        }
        for i in ls:
            # print(f"name: {i['title']}      id: {i['id']}")
            dataFile['name'].append(i['title'])
            dataFile['id'].append(i['id'])
        # create table
        table = tabulate(dataFile, headers=['name', 'id'], showindex=True)
        return table
    except:
        return 'error'

def mkdir_command(cmd):
    if len(cmd) != 3:
        return 'mkdir: missing operand. mkdir <folder_id> <name>'
    try:
        DriveFile('credentials_module.json').createFolder(cmd[1], cmd[2])
        return f'mkdir success crete folder [{cmd[2]}]'
    except:
        return f'error create {cmd[2]}'


def rm_command(cmd):
    if len(cmd) != 2:
        return 'rm: missing operand. rm <file_id>'
    try:
        DriveFile('credentials_module.json').removeFile(cmd[1])
        return f'rm success remove file [{cmd[1]}]'
    except:
        return f'error remove [{cmd[1]}]'


def get_command(cmd):
    if len(cmd) != 3:
        return 'get: missing operand. get <file_id> <path>'
    try:
        name_file = DriveFile('credentials_module.json').downloadFile(cmd[1], cmd[2])
        return f'download success file [{name_file}]'
    except:
        return f'error download [{cmd[1]}]'


def put_command(cmd):
    if len(cmd) != 3:
        return 'post: missing operand. post <id_folder> <path>'
    try:
        name_file = DriveFile('credentials_module.json').uploadFile(cmd[1], cmd[2])
        return f'upload success, file [{name_file}]'
    except:
        return f'error upload [{cmd[1]}]'


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
    else:
        return 'Command not found'


def main():
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
