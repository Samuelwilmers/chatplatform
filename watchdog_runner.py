import os
import time
from subprocess import call
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ChangeHandler(FileSystemEventHandler):
    """Ereignis-Handler, der auf Dateiänderungen reagiert und den Flask-Server neu startet."""
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('.py'):
            print(f'Änderung erkannt: {event.src_path}')
            call(['flask', 'run'])  # Beispiel für das Starten des Flask-Servers.

def start_observer():
    path = os.path.join(os.path.dirname(__file__), 'your_flask_app_directory')
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print(f'Beobachte Änderungen im Verzeichnis: {path}')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == '__main__':
    start_observer()
