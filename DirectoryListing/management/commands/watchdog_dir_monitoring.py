import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os, pytz
import django
from datetime import datetime
from django.core.management import BaseCommand
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DirectoryListing.settings")
#django.setup()
from DirectoryListing.models import FileRepository

#class Watcher:
class Command(BaseCommand):
    DIRECTORY_TO_WATCH = "/Users/Anubha.Vijay/Documents/dir_to_watch"

    def __init__(self):
        self.observer = Observer()

    #def run(self):
    def execute(self, *args, **options):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
            print ("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    def on_any_event(self,event):
        print (event.event_type)
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            print ("path{}".format(os.path.abspath(event.src_path)))

            filerepository = FileRepository(
                name=event.src_path.split('/')[-1],
                path=os.path.abspath(event.src_path),
                creation_time=datetime.fromtimestamp(os.path.getctime(event.src_path), tz=pytz.UTC),
                modified_time=datetime.fromtimestamp(os.path.getmtime(event.src_path), tz=pytz.UTC),
                size=os.path.getsize(event.src_path) // 100

            )
            filerepository.save()


            # Take any action here when a file is first created.
            print ("Received created event - {}.".format(event.src_path))

        elif event.event_type == 'modified':

            # Taken any action here when a file is modified.
            print ("Received modified event - {}.".format(event.src_path))

        elif event.event_type == 'deleted':
            # Taken any action here when a file is modified.
            print ("Received deleted event - {}".format(event.src_path))
            FileRepository.objects.filter(path=os.path.abspath(event.src_path)).delete()


#if __name__ == '__main__':
#    w = Watcher()
#    w.run()
