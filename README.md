# Notification app
- API written in Python with FastAPI.

#### Notes
- A notification system for push notification, SMS message and email

## Project Structure




## Setup the project locally
```sh
./run.sh
```
- Swagger API documentation is available in here: **http://127.0.0.1:8004/docs**
- The celery dashboard is available in here: **http://127.0.0.1:5557**

### Pre-populate the database
```sh
docker-compose exec notification_service python management.py recreate-db && \
docker-compose exec notification_service python management.py populate-db
```

## Tests
#### Run tests
```sh
./test.sh
```

#### Run tests with coverage
```sh
./test.sh cov
```
Note: The current coverage of the project is 99%


## Other commands
#### Format the code with back and isort
- You should run this command before a push
Note: It is possible to force this command in a pre-commit.
```shell
make format
```

#### Check code compliance
- You should run this command before a push
```shell
flake8 .
```

#### Get the logs
```shell
docker-compose logs -f
```


#### Stop the containers
```shell
docker-compose stop
```


## Next Steps
- I would add **pagination** to the endpoints and return the logs order by datetime. And add an 
  index for the column **created** in the table **log**. This solution would allow the application to scale
  with the increase of data in the database.
- I would add database migrations with Flask-Migrate library. This step can allow us to manage the changes in the 
  database 
  easily.
- I would add logs to the project to keep track of what's happening behind the scenes. 
- I would add the production configurations to run the project. For example, the SECRET_KEY, credentials for the 
  production database and other things.