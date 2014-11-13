#!python2
from __future__ import print_function
import shutil
import os
import getpass

NEWPATH = 'C:/users/'+getpass.getuser()+'/desktop/Alphaciv Backup/'

if os.path.exists(NEWPATH):
    shutil.rmtree(NEWPATH)
    
os.mkdir(NEWPATH)
    
for f in os.listdir('.'):
    if not f[f.rfind('.'):] == '.pyc':
        shutil.copy(f, NEWPATH+f)
