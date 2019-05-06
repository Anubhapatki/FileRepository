import os,time
from datetime import datetime
from django.core.management import BaseCommand
from DirectoryListing.models import FileRepository
from django.utils import timezone
import pytz


# Given a path to
class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('directory_name',help="Enter the directory name for creating the file repostory",
                             type=str )

    def execute(self, directory_name, *args, **options):
        directory_name = directory_name
        FileRepository.objects.all().delete()
        for root, dirs, files in os.walk(directory_name, topdown=True):
            print("\nfiles\n")
            for f in files:
                print(f,os.path.abspath(os.path.join(root, f)),os.path.getctime(os.path.join(root, f)),
                      os.path.getmtime(os.path.join(root, f)), os.path.getsize(os.path.join(root, f)))

                filerepository = FileRepository(
                    name=f,
                    path=os.path.abspath(os.path.join(root, f)),
                    creation_time=datetime.fromtimestamp(os.path.getctime(os.path.join(root, f)),tz=pytz.UTC),
                    modified_time=datetime.fromtimestamp(os.path.getmtime(os.path.join(root, f)), tz=pytz.UTC),
                    size= os.path.getsize(os.path.join(root, f))//100

                )
                filerepository.save()
            file_repo=FileRepository.objects.all()
            for f in file_repo:
                print (f.name, f.path, f.creation_time, f.modified_time, f.size)

            print ("\n")
        """
        files_path = [os.path.join(directory_name,x) for x in os.listdir(directory_name)]
        for f in files_path:
            if os.path.isfile(f):
                print (f)


                #print ("filename:{}", "path:{}", "created_on:{}", "last_modified:{}", "size:{}"
                #    .format("", f, os.stat(f).st_birthtime, os.stat(f).st_mtime, os.stat(f).st_size))
                print("\n")
        """
