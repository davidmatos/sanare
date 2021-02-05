import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from pymongo import MongoClient
from datetime import datetime


DB_INSTANCE = None
PATH_TO_WATCH = "/var/www/html"


def get_db():
    global DB_INSTANCE
    if DB_INSTANCE is None:
        client = MongoClient('mongodb://10.1.0.101:27017')
        DB_INSTANCE = client.sanare
    return DB_INSTANCE



def on_created(event):
    db = get_db()
    print(f"hey, {event.src_path} has been created!")

    fslogentry = {
                "ts": datetime.now(),
                "op": "created",
                "src_path": event.src_path,
                "event_type": event.event_type,
                "is_directory": event.is_directory
            }
    fslogentries = db.fslogentries
    fslogentries.insert_one(fslogentry)


def on_deleted(event):
    db = get_db()
    print(f"what the f**k! Someone deleted {event.src_path}!")
    fslogentry = {
            "ts": datetime.now(),
            "op": "created",
            "src_path": event.src_path,
            "event_type": event.event_type,
            "is_directory": event.is_directory
        }
    fslogentries = db.fslogentries
    fslogentries.insert_one(fslogentry)

def on_modified(event):
    db = get_db()
    print(f"hey buddy, {event.src_path} has been modified")
    fslogentry = {
            "ts": datetime.now(),
            "op": "created",
            "src_path": event.src_path,
            "event_type": event.event_type,
            "is_directory": event.is_directory
        }
    fslogentries = db.fslogentries
    fslogentries.insert_one(fslogentry)

def on_moved(event):
    db = get_db()
    print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")
    fslogentry = {
            "ts": datetime.now(),
            "op": "created",
            "src_path": event.src_path,
            "dest_path": event.dest_path,
            "event_type": event.event_type,
            "is_directory": event.is_directory
        }
    fslogentries = db.fslogentries
    fslogentries.insert_one(fslogentry)




if __name__ == "__main__":
    patterns = "*"
    ignore_patterns = ""
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    
    my_event_handler.on_created = on_created
    my_event_handler.on_deleted = on_deleted
    my_event_handler.on_modified = on_modified
    my_event_handler.on_moved = on_moved

    path = PATH_TO_WATCH
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)

    print("Starting watcher")

    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()