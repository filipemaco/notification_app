# Notification app
- API written in Python with FastAPI.


## Setup the project locally
```sh
./run.sh
```
- Swagger API documentation is available in here: **http://127.0.0.1:8004/docs**

### Pre-populate the database
```sh
docker-compose exec notification_service python management.py recreate-db && \
docker-compose exec notification_service python management.py populate-db
```

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

## Connect to the database
```shell
docker-compose exec db psql -U postgres
```
```
postgres=# \c notification
postgres=# select * from users; 
postgres=# \q 
```


## Added Libraries
- **pytest-cov** - Generate code coverage reports
- **Black** - Code formatting
- **isort** - Optimizes imports
- **Flake8** - Checks for PEP8 compliance