# encoding: utf-8

# library
import platform
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive


# class JSON
class DriveFile:
    def __init__(self, credentialsFile: str):
        # declare variables
        self.credentialsFile = credentialsFile

    def login(self):
        GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = self.credentialsFile
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile(self.credentialsFile)

        if gauth.credentials is None:
            gauth.LocalWebserverAuth(port_numbers=[8092])
        elif gauth.access_token_expired:
            gauth.Refresh()
        else:
            gauth.Authorize()

        gauth.SaveCredentialsFile(self.credentialsFile)
        drive = GoogleDrive(gauth)
        return drive

    def searchFile(self, query=None):
        drive = self.login()
        try:
            listFile = drive.ListFile().GetList()
            if query is not None:
                listFile = drive.ListFile({'q': query}).GetList()
            result = list()
            for f in listFile:
                result.append({'title': f['title'], 'id': f['id'], 'link': f['embedLink']})
                # r.append({f})
            return result
        except:
            pass

    def uploadFile(self, id_folder: str, ruta_file: str):
        drive = self.login()
        try:
            file = drive.CreateFile({'parents': [{"kind": "drive#fileLink",
                                                  "id": id_folder}]})
            slash_system = '\\' if platform.system().lower() == 'windows' else '/'
            file['title'] = ruta_file.split(f"{slash_system}")[-1]
            name = file['title']
            file.SetContentFile(ruta_file)
            file.Upload()
            return name
        except:
            pass

    def downloadFile(self, id_file: str, ruta_file: str):
        drive = self.login()
        try:
            file = drive.CreateFile({'id': id_file})
            name = file['title']
            file.GetContentFile(ruta_file + name)
            return name
        except:
            pass

    def removeFile(self, id_file: str, mode='trash'):
        drive = self.login()
        try: 
            file = drive.CreateFile({'id': id_file})
            if mode == 'trash':
                file.Trash()
            elif mode == 'outTrash':
                file.UnTrash()
            elif mode == 'permanent':
                file.Delete()
        except:
            pass

    def createFolder(self, id_folder, name_file):
        drive = self.login()
        try:
            newFolder = drive.CreateFile({'title': name_file, "parents": [{"kind": "drive#fileLink", "id": id_folder}],
                                          "mimeType": "application/vnd.google-apps.folder"})
            newFolder.Upload()
        except:
            pass