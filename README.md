# LocalizationTesting-CollabProject

Localization Testing program in collaboration with ARTRAX and UCM Computer Science Faculty.

The docker image to train is made by [jitesoft.](https://hub.docker.com/r/jitesoft/tesseract-ocr).

Before running the image, check the Dockerfile to ensure you have the same number of threads, or if different change the values from 12 to your
exact number of threads. The values are "12" in the "#Bulding tesseract" section.

To run the container and image sumply run Docker Desktop and type in a terminal inside trainingImage:

```
docker compose up -d
docker exec -it tesseract-cont bash
```

Then to stop and delete container simply type:

```
docker compose down
```

If you wish to delete also the image, add --rmi 'all' to the command 

