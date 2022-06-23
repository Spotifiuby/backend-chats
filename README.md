[![codecov](https://codecov.io/gh/Spotifiuby/backend-chats/branch/main/graph/badge.svg?token=AeF0yP6UgT)](https://codecov.io/gh/Spotifiuby/backend-chats) ![codecov](https://github.com/Spotifiuby/backend-chats/workflows/Spotifiuby%20CI/badge.svg)

# Table of Contents
* [Setup](#setup)
* [Environment Variables](#environment-variables)
* [Tests](#tests)
* [Run the docker container locally](#run-the-docker-container-locally)
* [Deploy](#deploy)
* [Docs](#docs)
* [Docker and Heroku](#docker-and-heroku)

# Setup
First, create a new python environment.
```
$ python3 -m venv venv
$ source ./venv/bin/activate
```

Now install all the requirements.
```
$ pip install -r requirements.txt
```

Finally, run the app.
```
$ uvicorn main:app --reload
```

If during development you add any dependency, remember to run:
```
pip freeze > requirements.txt
```

# Environment Variables
Create the `.env` file in the root folder of the project.\
It must contain the following environment variables.

Development environment:
```
CURRENT_ENVIRONMENT=development
```

Production environment:
```
MONGODB_USER={Mongo username}
MONGODB_PASSWD={Mongo password}
GOOGLE_APPLICATION_CREDENTIALS={Path to Google Credentials}
CURRENT_ENVIRONMENT=production
```

# Tests
For tests and coverage run the following.
```
coverage run -m pytest
coverage report
```

# Run the docker container locally

~~~
docker build -t backend-chats .
port=8000; docker run -e PORT=$port -p $port:$port backend-chats
~~~

# Deploy
## Setup
Create heroku remote.
```
heroku git:remote -a spotifiuby-backend-songs
```

## Manual Deploy
After any change, run.
```
git push heroku main
```

And get the server url with
```
heroku info
```

## SSH
Use Heroku Exec to connect to a dyno.
```
heroku ps:exec
```

Or
```
heroku ps:exec --dyno=web.2
```

# Docs
To read the interactive docs go to:\
http://127.0.0.1:8000/docs


# Docker and Heroku
**Note:** Replace `your-app-name` in the instructions with the name you wish to have on your app.

1. Install git (or just downlad the repo)

2. Install [Heroku cli](https://devcenter.heroku.com/articles/heroku-cli) and [log in](https://devcenter.heroku.com/articles/heroku-cli#getting-started)

3. Clone or download this repo.

```bash
git clone git@github.com:Spotifiuby/backend-chats.git
```

4. cd into the directory

```bash
cd backend-chats
```

5. Create the heroku app

```bash
heroku create your-app-name
```

6. Set the heroku cli git remote to that app

```bash
heroku git:remote your-app-name
```

7. Set the heroku stack setting to container

```bash
heroku stack:set container
```

8. Push to heroku

```bash
git push heroku main
```

9.  Enjoy your fastAPI app at [https://your-app-name.herokuapp.com](https://your-app-name.herokuapp.com)

*Ref:* https://github.com/askblaker/fastapi-docker-heroku
