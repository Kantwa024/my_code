from time import time
import firebase
from firebase_admin import db, storage
import time

# ref = db.reference("/query/1")
# ref.set(
#     {
#         'data': 'local search engine',
#         'cnt': 20,
#         'time': int(round(time.time() * 1000))
#     }
# )

ref = db.reference("/upload_file/1")
ref.set(
    {
        'address': 27972,
        'name': 'Local Search Engine.exe',
        'time': int(round(time.time() * 1000))
    }
)

def listener(event):
    if event.data != None:
        s = event.data['data']
        if s == 'uploaded':
            print('downloading')
            ref = db.reference("/upload_file/1")
            data = ref.get()

            bucket = storage.bucket()
            blob = bucket.blob(data['name'])
            blob.download_to_filename(r'C:\\Local Search\\files\\'+ data['name'])

            print('downloaded')


db.reference("/update/1").listen(listener)

