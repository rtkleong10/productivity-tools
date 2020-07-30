# Productivity Tools
- Productivity Tools is a project that contains various tools for enhancing productivity
- I created these tools because I was unable to find similar tools online
- This repository contains the backend server for Productivity Tools
    - It uses Django Rest Framework and has a browsable API
- You can view it live [here](https://rtkleong10-productivity-tools.herokuapp.com/)
    - The server is hosted using Heroku
    - It make take some time to load initially as Heroku lets the server sleep if it's not in use for some time
- It provides API endpoints for the [frontend web app](https://github.com/rtkleong10/productivity-tools-web/)


## Tools
> You can find more info in the wiki
- [Days Since](https://github.com/rtkleong10/productivity-tools/wiki/Days-Since)
- [Time Cycles](https://github.com/rtkleong10/productivity-tools/wiki/Time-Cycles)

## How to Run Locally
1. Install Python
2. `pip install -r requirements.txt`
3. Change `DEBUG = False` to `DEBUG = True`
4. `python manage.py migrate`
5. `python manage.py runserver`
    1. After the first run, you only need to do this step for future runs

## Resources
- Favicon is a modified version of a [Flaticon icon](https://www.flaticon.com/free-icon/clock_2784459)
