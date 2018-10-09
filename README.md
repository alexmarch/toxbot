# Demo ToxBot

## Build / Run
Run install local with python3
```bash
    python -m envv envv
    . ./venv/bin/activate
```
Up and run application local
```bash
    FLASK_APP=src/api FLASK_ENV=development flask run
```
## Get Tox ID
After running application you can open log file located in data folder and check Tox ID.
Then you can add this tox id to your application android/iphone/osx/win.

## Configuration
In .env file you can find all options for bot app.
For SSL you need generate cert/key and set USE_SSL=1
For Sock2 proxy you can setup option PROXY_TYPE=2