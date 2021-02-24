from __future__ import print_function
import httplib2
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os, io

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
import auth
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
authInst = auth.auth(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME)
credentials = authInst.getCredentials()

http = credentials.authorize(httplib2.Http())
drive_service = discovery.build('drive', 'v3', http=http)

def listFiles(size):
    results = drive_service.files().list(
        pageSize=size,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))

def uploadFile(filename,filepath,mimetype):
    file_metadata = {'name': filename}
    media = MediaFileUpload(filepath,
                            mimetype=mimetype)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print('File ID: %s' % file.get('id'))


def createFolder(name):
    file_metadata = {
    'name': name,
    'mimeType': 'application/vnd.google-apps.folder'
    }
    file = drive_service.files().create(body=file_metadata,
                                        fields='id').execute()
    print ('Folder ID: %s' % file.get('id'))


app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/upload')
def upload_file():
   return render_template('upload.html')

@app.route('/uploader', methods = ['POST'])
def uploader_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(app.root_path, 'Reto', secure_filename(f.filename)))
        uploadFile(f.filename,"Reto/"+f.filename,"/."+f.filename.split(".")[1])   

    return render_template('index.html', msg = "file loaded successfully")

@app.route('/crearc')
def crearc():
   return render_template('crearCarpeta.html')

@app.route('/creadorc', methods = ['GET' ,'POST'])
def creadorc():
    nombre = request.args.get('nombre')  
    createFolder(nombre)
    return render_template('index.html', msg = "folder loaded successfully")

if __name__ == '__main__':
   app.run(debug = True)

#uploadFile('unnamed.jpg','unnamed.jpg','image/jpeg')
#createFolder('Google')
#uploadFile('prueba.txt', 'Reto/prueba.txt','text/txt')
listFiles(3)