import datetime
import logging
import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler  # change event handler base class
from watchdog.observers import Observer


# Here we are overriding of Class FileSystemEventHandler
class UserHandler(FileSystemEventHandler):

    def __init__(self, logging_path):
        self.logging_path = logging_path

    def on_moved(self, event):  # Executed when a file or directory is moved
        super().on_moved(event)
        current_time = str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
        catalogue = 'catalogue' if event.is_directory else 'file'
        with open(self.logging_path, 'a+') as logg:
            logg.write(f"{current_time} Renamed {catalogue}: from {event.src_path} in {event.dest_path}\n")
        print(f"{current_time} Renamed {catalogue}: from {event.src_path} in {event.dest_path}\n")

    def on_created(self, event):  # Executed when a file or a directory is created
        super().on_created(event)
        current_time = str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
        catalogue = 'catalogue' if event.is_directory else 'file'
        with open(self.logging_path, 'a+') as logg:
            logg.write(f"{current_time} Created {catalogue}: {event.src_path}\n")
        print(f"{current_time} Created {catalogue}: {event.src_path}\n")

    def on_modified(self, event):  # Executed when a file is modified or a directory renamed
        super().on_modified(event)
        current_time = str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
        catalogue = 'catalogue' if event.is_directory else 'file'
        with open(self.logging_path, 'a+') as logg:
            logg.write(f"{current_time} Changed {catalogue}: {event.src_path}\n")
        print(f"{current_time} Changed {catalogue}: {event.src_path}\n")

    def on_deleted(self, event):  # Executed when a file or directory is deleted.
        super().on_deleted(event)
        current_time = str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
        catalogue = 'catalogue' if event.is_directory else 'file'
        with open(self.logging_path, 'a+') as logg:
            logg.write(f"{current_time} Deleted {catalogue}: {event.src_path}\n")
        print(f"{current_time} Deleted {catalogue}: {event.src_path}\n")


def log(logging_path, source):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    path = Path(source).resolve()
    observer = Observer()
    observer.schedule(UserHandler(logging_path), path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
