import sys
import os
from firebase_admin import credentials, initialize_app,storage
# Initialize Firebase Admin SDK

# This will correctly locate your bundled file at runtime
if getattr(sys, 'frozen', False):
    # We are running in a PyInstaller bundle
    base_path = sys._MEIPASS
else:
    # We are running in a normal Python environment
    base_path = os.path.abspath(".")

# Load your data file from the base path
json_file_path = os.path.join(base_path, 'firebase_data\\credentials.json')
cred = credentials.Certificate(json_file_path)
print(json_file_path)
app = initialize_app(cred, {'storageBucket': 'docsspace-f400a.appspot.com'})
bucket = storage.bucket()