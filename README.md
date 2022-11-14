# Notification app
- An internal notification system for push notification (Android and iOS), SMS message and email. The API written in 
  Python with FastAPI.
- It is possible to add/change/delete the user information (id, email, phone_number)
- It is possible to create notifications for the users and check the status of the notification.


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

#### Bring down the containers and volumes
```shell
docker-compose down -v
```


## Next Steps
- Add more functionalities to the endpoints. Example: Filter message by status.
- Add database migrations with Alembic library. This step can allow us to manage the changes in the 
  database easily.
- Add logs to the project to keep track of what's happening behind the scenes. 
- Add the production configurations to run the project.