import sys
import os
from firebase_admin import credentials, initialize_app,storage
from firebase_admin.storage import bucket

# This will correctly locate your bundled file at runtime
_BASE_PATH_ = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.abspath(".")

# setup firebase connectivity
_JASON_FILE_PATH_ = os.path.join(_BASE_PATH_, 'firebase_data\\credentials.json')
_FIREBASE_CREDENTIALS_ = credentials.Certificate(_JASON_FILE_PATH_)
_STORAGE_OPTIONS_ = {'storageBucket': 'docsspace-f400a.appspot.com'}
_FIREBASE_DIR_= 'images'
app = initialize_app(_FIREBASE_CREDENTIALS_, _STORAGE_OPTIONS_)
bucket = storage.bucket()
