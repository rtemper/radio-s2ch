# Installation
In order to run the project the following things will required:
* mpd
* icecast
* mpc
* postgres
* radio-s2ch backend
  * django server
  * redis
  * celery
  * mpd-watcher
* radio-s2ch frontend

## mpd
We will setup mpd with two streams. The first stream would be used for main content, and the second stream would be used as fallback.
* install mpd package with `pacman -S mpd`
* add mpd user with `adduser mpd`
* create directory for music `mkdir /home/mpd/music`
* create directories for streams `mkdir -p /home/mpd/playlist/stream{1,2}` 
* copy both `dist/config/mpd-streamX.conf` files to `/etc/mpd-streamX.conf`
* copy `dist/service/mpd@.service` to `/usr/lib/systemd/system/mpd@.service`
* run mpd streams with `systemctl start mpd@stream{1,2}`

at this point you should have two process listening `6601` and `6602` ports in top of `netstat -plant`

## icecast
Icecast used there to share mpd stream with other clients.
* install icecast with `pacman -S icecast`
* copy `dist/config/icecast.xml` to `/etc/icecast.xml`
* run icecast with `systemctl start icecast`

at this point you should have working icecast web server there `http://127.0.0.1:8765/`

## mpc
Mpc used there to control playlist manually (for debug purposes).
* install mpc package `pacman -S mpc`
* add some music into `/home/mpd/music` directory
* update mpd (stream1) database with `mpc --port 6601 update`
* add single track to mpd (stream1) queue `mpc --port 6601 ls | head -n1 | mpc --port 6601 add`
* play track `mpc --port 6601 play`

at this point you should be able to listen something at `http://127.0.0.1:8765/stream1.mp3`

## postgres 
Postgres used there to store tracks metadata and other stuff. Django ORM is used in top of that, so we need only basic user with assigned database.
(use additional resourses to install postgres cluster)
* install postgres
* create user `radio_admin` with password `radio_admin` 
* create database `radio` and grant all privileges to `radio_admin` 
* setup `pg_hba.conf` to allow localhost connections

at this point you should be able to connect to database `radio` as user `radio_admin` from `psql`, for example `psql -U radio_admin radio`

## radio-s2ch backend

For development purposes we need to run:
* virtualenv
* django server
* redis
* celery
* mpd-watcher

### virtualenv 
* install virtualenv (if required)
* create new virtual environment
* configure autoimport for `backend/backend/env/dev` file each time virtualenv is activated
* activate virtual environment

Note: you should use virtualenv for all the commands below 

### django server 
* open backend directory `cd backend`
* install project requirements with `pip install -r requirements.txt`
* migrate database with `python manage.py migrate`
* create superuser with `python manage.py createsuperuser`
* run development server with `python manage.py runserver`

at this point you should be able to open `http://127.0.0.1:8000/admin/` and login with your credentials. 

### redis
Redis server user for storing temporal data, like host requests and current track metadata. 
* install and run redis server
* check (and fix if required) redis host and port in `backend/backend/env/dev` file
* run redis server

### celery
Celery used for background tasks like upload-from-youtube.
* run `celery -A backend worker --loglevel=info` from the `backend` folder
* you should see something like `[tasks]` `. radio.tasks.add_to_queue_from_youtube` in result

at this point backend will be able to handle youtube requests
 
### mpd-watcher
Mpd watcher is a custom script that listens mpd daemon events and sends appropriate data to frontend. It updates frontend details like current track name.
* run `python -m backend.scripts.watcher`

at this point any mpd activity would be displayed in the shell. Try to change current track to see this.


## radio-s2ch frontend 
* install `nodejs` 
* navigate to `frontend` directory 
* install all the required packages with `npm install` 
* run development server with `webpack-dev-server`
* open `127.0.0.1:8080` in a browser

if all the things configured well, you will be able to send requests and listen audio. When no requests are presented, tracks will be offered automatically.

