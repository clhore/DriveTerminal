# encoding: utf-8

# library
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
        listFile = drive.ListFile().GetList()
        if query is not None:
            listFile = drive.ListFile({'q': query}).GetList()
        r = list()
        for f in listFile:
            r.append({"title": f['title'], "id": f['id'], "link": f['embedLink']})
            # r.append({f})
        return r

    def uploadFile(self, id_folder: str, ruta_file: str):
        drive = self.login()
        file = drive.CreateFile({'parents': [{"kind": "drive#fileLink",
                                              "id": id_folder}]})
        file['title'] = ruta_file.split("/")[-1]
        name = file['title']
        file.SetContentFile(ruta_file)
        file.Upload()
        return name

    def downloadFile(self, id_file: str, ruta_file: str):
        drive = self.login()
        file = drive.CreateFile({'id': id_file})
        name = file['title']
        file.GetContentFile(ruta_file + name)
        return name

    def removeFile(self, id_file: str):
        drive = self.login()
        file = drive.CreateFile({'id': id_file})
        # delete file
        file.Delete()

    def createFolder(self, id_folder, name_file):
        drive = self.login()
        newFolder = drive.CreateFile({'title': name_file, "parents": [{"kind": "drive#fileLink", "id": id_folder}],
                                      "mimeType": "application/vnd.google-apps.folder"})
        newFolder.Upload()
