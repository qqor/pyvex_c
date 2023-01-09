import os
import subprocess
import sys
import shutil
import multiprocessing
import platform

PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))
PAR_DIR = os.path.dirname(PROJECT_DIR)
VEX_PATH = os.path.abspath(os.path.join(PAR_DIR, 'vex'))

e = os.environ.copy()
e['VEX_LIB_PATH'] = VEX_PATH
e['VEX_INCLUDE_PATH'] = os.path.join(VEX_PATH, 'pub')
e['VEX_LIB_FILE'] = os.path.join(VEX_PATH, 'libvex.lib')

if sys.platform == 'win32':
    cmd = ['nmake', '/f', 'Makefile-msvc']
elif shutil.which('gmake') is not None:
    cmd = ['gmake', '-f', 'Makefile', '-j', str(multiprocessing.cpu_count())]
else:
    cmd = ['make', '-f', 'Makefile', '-j', str(multiprocessing.cpu_count())]

# TODO: maybe move this to parent dir? 
try:
    subprocess.run(cmd, env=e, check=True)
except FileNotFoundError as err:
    raise LibError("Couldn't find " + cmd[0] + " in PATH") from err
except subprocess.CalledProcessError as err:
    raise LibError("Error while building libpyvex: " + str(err)) from err
