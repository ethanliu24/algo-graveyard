# Algo Graveyard


## Overview
Algo Graveyard is a full stack application where my inefficient and disappointing algorithms rests.

It is a personal web application to organize algorithm questions and solutions. Powered by a FastAPI backend and React frontend, it supports CRUD operations, custom web parsing from platforms like LeetCode, and is optimized for single-user usage.


## Features
- Question and solution CRUD management
- Filter and sort questions
- Web parsing to extract details of questions (currently only supports LeetCode)
- AI generated analysis of each provided solution
- Admin authentication to access entry management


## Installation
First clone the [repository](https://github.com/ethanliu24/algo-graveyard) and step into it. Follow the rest of the steps to set up the project.


### Software dependencies
- [Python 3.11+](https://www.python.org/downloads/)
- [Node.js](https://nodejs.org/en/download)
- [Weasyprint](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html)


### Database set up
The project uses Firebase's Firestore service as the database.

1. Create a new project in [firebase](https://firebase.google.com/) with your google account.
2. Acquire a private key for firestore (Home > project settings service accounts > Choose python > Generate new private key).
3. Put the private key in the root and name it `firebase-key.json`.
4. In the environment file, paste `localhost:8080` to `FIRESTORE_EMULATOR_HOST`. This is required for developement and test environments.


### AI analyzer set up
The project uses Gemini to generate analyses for solutions.

1. Get started with [Gemini](https://ai.google.dev/) with the same google account used for Firebase.
2. Bind with the Firebase project (which is in the google cloud in the account you signed up with).
3. Generate an API key and copy it to `GEMINI_API_KEY` in the environment files.
4. In the environment file, use a prefered Gemini model (suggested model: `gemini-2.0-flash`) in `GEMINI_MODEL`.


### Create virtual environment
Create a Python virtual environment with the command `python3 -m venv .venv`

Notes:
1. Change the Python interpreter to the .venv folder that's created. In VS Code, do `Ctrl/Cmd + Shift + P`, type in `Python: Select Interpreter` and select the current environment.
2. Optional, but if you don't want `__pycache__/` directories, go to `.venv/bin/activate` and paste in `export PYTHONDONTWRITEBYTECODE=1` somewhere.
3. Check if you are in the right virtual environment with command: `which python3`. This should return a path to the virtual environment.


### Installing dependencies
Run the following commands to install all required dependencies.
```
# backend dependencies (make sure to run this in the virtual environment!)
$ pip install -r requirements.txt

# frontend dependencies
$ npm install

# firebase cli
npm install -g firebase-tools@latest

# web parsing dependencies
$ playwright install chromium chrome
```


## Running the app
You will need at least 3 terminals.


### Terminal 1 - Firebase emulator
This terminal will host an emulator for all firebase services. You can see it if you navigate to `http://localhost:4000/` in your browser.

Run the command:
```
$ firebase emulators:start --import=db_seeds/dev_data --export-on-exit=db_seeds/dev_data
```
Note that you can replace the path for `--import` and `--export-on-exit` to a desired path. `--export-on-exit` saves new changes to the given directory and `--import` imports data exported from a previous session. Not including those flags will start with an empty database every session.

Stop the emulator with command `Ctrl/Cmd + C`


### Terminal 2 - Front end
This terminal will watch for any changes to the front end.

Run the command:
```
$ npm run dev  # keep it running
```

Stop the watch with command `Ctrl/Cmd + C`


### Terminal 3 - Server
This terminal runs the server.

First, enter the virtual environment if not already in:
- MacOS & Linux: `source .venv/bin/activate`
- Windoes Powershell: `.venv\Scripts\Activate.ps1`
- Windows Bash: source `.venv/Scripts/activate`

You can exit the virtual environment with the command `deactivate`.

Start the server with command:
```
fastapi dev
```

Stop the server with `Ctrl/Cmd + C`


### Terminal 4 - Other
You can use this terminal to commit, run tests, etc.


## Tests
```
# run all tests
$ pytest

# run all tests in the given directory or file
$ pytest tests/<dir_to_file_or_dir>
```


## Testing in Staging
Local tests and checks before deploying to production.

Notes:
- At staging enviornment, hosts on port 0.0.0.0.80, which is not HTTPS. Since the JWT in cookie is set to `Secure=True`, it won't save any cookie. Set it to false to test, but remember to set it back to true.
- Set `APP_ENV` to `staging` so the app looks at the correct path for firebase secret key (The file location is different on Render).
- Use `.env.staging` env file. The content should be the same as `.env.production` except `APP_ENV`.

```
# build an image
docker build -t algograveyard .

# run the container
docker run -d \
   --name algograveyard \
   --env-file=./.env.staging \
   -v ./firebase-key.json:/algograveyard/firebase-key.json \
   -p 80:80 algograveyard
```


## Contributing
This project is designed for personal use and maintenance, so I won't be accepting external contributions.
