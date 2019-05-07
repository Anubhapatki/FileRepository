# FileRepository
FileRepository which holds files last 5 days, rest are archived and provides an API using Django Rest Framework for accessing the files.

### Prerequisites

Create a virtual environment and activate it

```
python3 -m venv env
```

```
source env/bin/activate
```

### Installing Requirements

Make sure you are in the main directory. Install the requirements.txt using pip install.

```
pip install -r requirements.txt
```
### Create a superuser

You will need a superuser account for administration purposes.

```
python manage.py createsuperuser
```

### Run the server & login


```
python manage.py runserver
```

### Implementation Details

I have used Django, Django Rest Framework, Watchdog and Celery for the implementation of the project.

1. Read the information of the files in a directory (name, path, creation date/time, modification
date/time and size)

    Used Django Management Command to check the directory name provided using os.walk and read the above parameters

    ```
    python manage.py get_directory_listing <dir_name>
    ```

2. Import the data into a PostgreSQL/MySQL/MongoDB databases. The result should be one
 table or collection to store this information.

    Store the details in Django Model FileRepository table. The above management command does both read and storing in the model.

3. Monitor the directory to see if there are new files or changes in existing ones. (You can use
cronjobs, infinite loops with parallel threads or any other solution that you consider)

    Used watchdog(https://pythonhosted.org/watchdog/) Python library to monitor various filesystem events. The management 
    command watchdog_dir_monitoring polls the desired library every second and looks for any events and updates the Filerepository 
    table accrodingly.

    ```
    python manage.py watchdog_dir_monitoring <dir_name>

    ```
4. Archive the oldest files (more than 5 days). You should consider having a new field in the
database table or move the files to another directory.

    Used Celery Aysnchronous Queus with Redis Message Broker, for archiving any files which are more then old in the FileRepository.
    Celery Runs a periodic task every 5 days updates the Filerepository 'archived' flag and archived data field. This could be achieved 
    using a management commands and cron job as well. But if we talk about scalability and deploying this app of production environment 
    then monitoring and periodic tasks can be carried out in background without disturbing the request response.
    
    Download and start redis server
    
    ```
    redis-server
    redis-cli ping - it should print pong 
    ```
    Start the celery worker
    ```
    celery -A FileRepo worker -l Debug
    ```
    Start celery beat
    ```
    celery -A FileRepo beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
    ```
    
 5. Develop an small web API with two endpoints to: get a JSON object with the avaiable files
    and get a JSON object with archived files.
    
    Used Django RestFramework to create the two endpoints which would list the available and archived files. The Integration tests 
    for these are available in DirectoryListing/tests.py. Due to time contraints I have not applied any authentication on the APIs.
    
    ```
    http://localhost:8000/api/available_files
    http://localhost:8000/api/archived_files
    ```
    Caching can also be applied to these, although the data is quite dynamic so caching of few seconds can be applied if network 
    load is high
    
    
   
    





