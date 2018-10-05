# Demo ToxBot

## Build / Run
Build container
```bash
    docker-compose build -t toxbot
```
Up and run container
```bash
    docker-compose up toxbot -d
```
## Get Tox ID
After running application you can open log file located in data folder and check Tox ID.
Then you can add this tox id to your application android/iphone/osx/win.

## Configuration
In .env file you can find all options for bot app.
For SSL you need generate cert/key and set USE_SSL=1
For Sock2 proxy you can setup option PROXY_TYPE=2