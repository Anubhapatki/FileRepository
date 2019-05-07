import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os, pytz
import django
from datetime import datetime
from django.core.management import BaseCommand
from DirectoryListing.models import FileRepository

#class Watcher:
class Command(BaseCommand):


    def __init__(self):
        self.observer = Observer()

    def add_arguments(self, parser):
        parser.add_argument('directory_name',help="Enter the directory name for creating the file repostory",
                             type=str )

       # DIRECTORY_TO_WATCH = "/Users/Anubha.Vijay/Documents/dir_to_watch"

    #def run(self):
    def execute(self, directory_name, *args, **options):
        event_handler = Handler()
        self.observer.schedule(event_handler, directory_name, recursive=True)
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
        if event.is_directory and event.src_path.split('.')[-1] == "swp":
            return None

        elif event.event_type == 'created':
            print ("path{}".format(os.path.abspath(event.src_path)))
            try:
                filerepository = FileRepository(
                    name=event.src_path.split('/')[-1],
                    path=os.path.abspath(event.src_path),
                    creation_time=datetime.fromtimestamp(os.path.getctime(event.src_path), tz=pytz.UTC),
                    modified_time=datetime.fromtimestamp(os.path.getmtime(event.src_path), tz=pytz.UTC),
                    size=os.path.getsize(event.src_path)

                )
                filerepository.save()
            except:
                print ("File could not be saved{}".format(event.src_path))
                pass


            # Take any action here when a file is first created.
            print ("Received created event - {}.".format(event.src_path))

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            print("Received modified event - {}.".format(event.src_path))
            try:
                file = FileRepository.objects.get(path=os.path.abspath(event.src_path))
                file.modified_time = datetime.fromtimestamp(os.path.getmtime(event.src_path), tz=pytz.UTC)
                file.save()
            except:
                print("File Source could not be seen{}".format(event.src_path))


        elif event.event_type == 'deleted':
            # Taken any action here when a file is modified.
            print ("Received deleted event - {}".format(event.src_path))
            try:
                FileRepository.objects.filter(path=os.path.abspath(event.src_path)).delete()
            except:
                print("File Source could not be seen{}".format(event.src_path))

        elif event.event_type == 'moved':
            # Taken any action here when a file is modified
            print ("Received moved event - {}.".format(event.src_path))
            try:
                file = FileRepository.objects.get(path=os.path.abspath(event.src_path))
                file.modified_time = datetime.fromtimestamp(os.path.getmtime(event.src_path), tz=pytz.UTC)
                file.save()
            except:
                print ("File Source could not be seen{}".format(event.src_path))




