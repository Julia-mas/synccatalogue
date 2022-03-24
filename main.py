import os
import shutil
from threading import Thread

from sync_log import *


def get_timer():
    while True:
        timer = input('Enter the statistics collection interval in seconds:\n')
        if timer.isdigit():
            return int(timer)
        else:
            print('Invalid time input format.')


def enter_info():
    while True:
        def get_path(num):
            while True:
                if num == 1:
                    text = 'Enter the path to the source directory.\n'
                elif num == 2:
                    text = 'Enter the path to the replica directory.\n'
                else:
                    text = 'Enter the path to the log file.\n'
                cpath = input(text)
                if os.path.exists(cpath):
                    return cpath
                else:
                    print('Invalid path specified.')

        path1 = get_path(1)
        path2 = get_path(2)
        if path1 != path2:
            path3 = get_path(3)
            return path1, path2, path3
        else:
            print('The location of the source directory and the replica directory is the same.')


def synch(sour_catalog, repl_catalog):
    timer = get_timer()
    if not sour_catalog.endswith('/'):
        sour_catalog += '/'
    if not repl_catalog.endswith('/'):
        repl_catalog += '/'
    while True:
        files = os.listdir(sour_catalog)
        files2 = files.copy()
# cleaning the contents of the replica directory
        for root, dirs, files in os.walk(repl_catalog):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
# synchronization of the replica directory with the source
        for f in files2:
            if '.' not in f:
                shutil.copytree(sour_catalog + f, repl_catalog + f)
            else:
                shutil.copyfile(sour_catalog + f, repl_catalog + f)
        time.sleep(timer)


source, replica, log_path = enter_info()
t1 = Thread(target=synch, args=(source, replica,))
t2 = Thread(target=log, args=(log_path, source,))
t1.start()
t2.start()

