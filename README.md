# Python Football Tools

This is a small project meant to make analzying football stats easy / fun.

Although not strictly required, this project is set up to use Docker
to get up and running quickly on any environent.

##  Using Docker
Make sure docker and docker compose are installed on your system (this task is left to the reader ;)

Build you football tools docker environment:
```
docker-compose build
docker-compose up -d
```
The -d flag tells runs the docker processes as daemons. If you want to see
everything in action, ommit the flag.

Next, you must jump into the python shell to build your database
(this will eventually be automated.  Perhaps you, dear reader, will add this)

To enter a running python container
find the container id using docker ps (should resemble football_tools_web)
and run:

```
docker exec -it <container id> /bin/bash
```

This will open a bash shell in the container running the django application.

To build your database, run the database migrations

```
python manage.py migrate
```

Finally, fill your database with players / stats
(for now, only includes 2015 season, easy to extend though)

```
./manage.py build_teams_and_players
./manage.py calculate_weekly_scores
```
