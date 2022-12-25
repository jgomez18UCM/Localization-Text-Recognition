# LocalizationTesting-CollabProject

Localization Testing program in collaboration with ARTRAX and UCM Computer Science Faculty.

The docker image to train is made by [jitesoft.](https://hub.docker.com/r/jitesoft/tesseract-ocr) 

To run the container and image sumply run Docker Desktop and type in command line:

```
docker compose up -d
docker exec -it tesseract-cont bash
```

Then to stop and delete container simply type:

```
docker compose down
```

If you wish to delete also the image, add --rmi 'all' to the command 

