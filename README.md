# DJango-PictureShareService

To run the web-server please do the following steps.
It is assumed here that you run on the Debian-like GNU Linux operating system.

1. Install required packages
```
sudo apt-get install git sqlite3 python3-venv python3-dev libpng-dev zlib1g-dev libjpeg-dev Python3-pil build-essential autoconf libtool pkg-config python-imaging
```

2. get the repository to the local folder (create if needed and cd to that directory)

```git clone https://github.com/dolv/DJango-PictureShareService.git```

3. go inside the newly created folder

```cd DJango-PictureShareService```

4. Create virtual environment instance

```python3 -m venv PictureShareServiceVENV```

5. Give execution rights to the activate script

```chmod +x PictureShareServiceVENV/bin/activate```

6. Activate working virtual environment (pay attention to the leading (.) dot)

```. PictureShareServiceVENV/bin/activate```

7. install project requirements as follows

```pip install -r requirements.txt```

8. check what packages where installed and compare it to the requirements.txt file

```pip freeze```

(the output should coincide with the requirements.txt content)

9. Prepare/create database tables running the following command:

```python manage.py migrate```

10. check if database has been appropriately initialed.

```
python manage.py dbshell

sqlite> .tables

```
you should see the console output similar to the following one:
```
SQLite version 3.8.11.1 2015-07-29 20:00:57
Enter ".help" for usage hints.
sqlite> .tables
Core_likes                  auth_user_groups
Core_picture                auth_user_user_permissions
PictureWithLikesCount       django_admin_log
auth_group                  django_content_type
auth_group_permissions      django_migrations
auth_permission             django_session
auth_user
```
```sqlite> .quit```

11. create superused for the database

```python manage.py createsuperuser```

12. Run the development server with the command:

```python manage.py runserver &```

The output will look like this:

```
Performing system checks...

System check identified no issues (0 silenced).
May 29, 2018 - 15:15:02
Django version 2.0.5, using settings 'PictureShareService.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

13. try connecting to http://127.0.0.1:8000/ in web-browser.

Have fun...

## Using with Dokcer
1. Build docker image e.g. like this:
```
docker build --force-rm --rm -t picture-share-service .
```

2. Run the container mapping local folder for persistance data.
```
docker run --rm --name picture-service -p 8080:8000 --env-file ./EnvVars/develop -v /app/DB:/app/DB -v /app/test_pictures:/app/media -v /app/test_pictures:/app/static picture-share-service 
```
3. Initialise the db, create superuser for the database and collect staticfiles.
```
docker exec -ti picture-service /bin/bash -c ". ../VirtualENV/bin/activate && python3 manage.py migrate"
docker exec -ti picture-service /bin/bash -c ". ../VirtualENV/bin/activate && python3 manage.py createsuperuser"
docker exec -ti picture-service /bin/bash -c ". ../VirtualENV/bin/activate && python3 manage.py collectstatic"
```
4. Connect to your application via http://localhost:8080/