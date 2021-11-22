# encoding: utf-8

# library
from pydrive.auth import GoogleAuth


def login():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Creates local webserver and auto handles authentication.
