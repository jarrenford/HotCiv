#!python2
from __future__ import print_function
import shutil
import os
import getpass

NEWPATH = 'C:/users/'+getpass.getuser()+'/desktop/Alphaciv Backup/'
BACKUP = """#!python2
import shutil
import os
import getpass

NEWPATH = 'C:/users/'+getpass.getuser()+'/desktop/Alphaciv Backup/'
BACKUP = ''
if os.path.exists(NEWPATH):
    shutil.rmtree(NEWPATH)
    
os.mkdir(NEWPATH)
    
for f in os.listdir('.'):
    if not f == "backup.py":
        shutil.copy(f, NEWPATH+f)

with open(NEWPATH+'backup.py', 'w') as f:
    print(BACKUP, file=f)"""

if os.path.exists(NEWPATH):
    shutil.rmtree(NEWPATH)
    
os.mkdir(NEWPATH)
    
for f in os.listdir('.'):
    if not f == "backup.py":
        shutil.copy(f, NEWPATH+f)

with open(NEWPATH+'backup.py', 'w') as f:
    print(BACKUP, file=f)
