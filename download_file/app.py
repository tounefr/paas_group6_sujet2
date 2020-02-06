
import urllib.request
import os

url = os.environ['DOWNLOAD_FILE_URL']
file_dest = os.environ['DOWNLOAD_FILE_DEST']
urllib.request.urlretrieve(url, file_dest)
