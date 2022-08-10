## User Service

This is a tiny microservice which stores the user information.
The user data is stored in memory so it is **only available during the app is running**.


### Important Points

The app is also an awfully written legacy service with some issues
- It takes 3 to 5s before the app starts.
- It crashes about 20% of the time when it starts.
- `ping` endpoint sometimes can cause high latency (maximum of 5s).

Take these into accounts when you are fulfilling the requirements.

### Setting up Python and installing Dependencies

- If you already have Python installed on your System and can use [venv](https://docs.python.org/3/library/venv.html#module-venv), feel free to use it.
- Otherwise, you can install any version above Python 3.8+ with [pyenv](https://github.com/pyenv/pyenv).
- After that, install the dependency provided in `requirements.txt`.
    - There is only one dependency: [Tornado](https://www.tornadoweb.org/en/stable/).

### Running the app

After you have installed the dependencies, you can run it by

```bash
# either run it from the top directory
python user-service/app.py

# or switch to the user-service folder
cd user-service
python app.py
```

This will run the app at port 8001.

### API Endpoints

#### Create a user

Endpoint: `POST /v1/users`

```bash
curl -XPOST "localhost:8001/v1/users" -F name="Admin" -F email="admin@gmail.com"
```

Example response:
```json
{"user_id":"4d3w1b28bt"}
```

#### Get all users

Endpoint: `GET /v1/users`

```bash
curl -XGET "localhost:8001/v1/users"                                            
```

Example response:
```json
{"users":{"4d3w1b28bt":{"email":"admin@gmail.com","name":"Admin"}}}
```

#### Get a single user

Endpoint: `GET /v1/users/<user_id>`

```bash
curl -XGET "localhost:8001/v1/users/4d3w1b28bt"
```

Example response:
```json
{"user":{"email":"admin@gmail.com","name":"Admin"}}
```

#### Ping

Use this endpoint for healthchecks!

Endpoint: `GET /ping`

Example response:
```
Ok!%
```
