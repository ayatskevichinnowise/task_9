## task_9 ##

### Start alert system ###

You can start it with 
```
docker compose up
```

And if you want to get email notifications from airflow with error description you should create **.env** file with next content
```
EMAIL=<your_email>
PASSWORD=<your_password>
```

### Description ###

This alert system waits for a file with new logs every hour. Then the alert system reads it and checks it for errors. 
Also we have a folder 'data' that includes two folders like 'bad' and 'good'. 
Then if our log file doesn't have errors it moves to 'good' folder with adding timestamp to its name.
If a log file contains errors it moves to 'bad' folder also with adding timestamp to its name and raising error with description of errors.
If system gets error raising it sends email notifications to email what your set in .env

### DAG ###

![dag-alert](https://user-images.githubusercontent.com/121276417/219425727-e4f1fb09-829e-4525-b475-466fb6175ca5.png)
