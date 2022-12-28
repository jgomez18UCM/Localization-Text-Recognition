# Running Tesseract Training Tools Image
Before running the image, check the Dockerfile to ensure you have the same number of threads, or if different change the values from 12 to your
exact number of threads. The values are "12" in the "#Bulding tesseract" section.

### Pre-work 
Copy desired files to sharedFolder in order to work with them inside container, and keep persistency to they don't get deleted when container shutsdown.

## Start Image and Run
To run the container and docker image simply run Docker Desktop and type in a terminal inside ./training folder:

**NOTE: It could take around 10min to build the image** 
```
docker compose up -d
docker exec -it tesseract-cont bash
```

## Training
Copy custom font file inside /usr/local/share/fonts and run the following command so the OS recognize the font.
```
fc-cache -f -v
```

Copy desired lenguage traineddata to tesseract/tessdata/

Create ground-truth for desired custom font using python script.

Go to tesstrain and run with custom font and number of iterations:

```
TESSDATA_PREFIX=../tesseract/tessdata make training MODEL_NAME=Apex START_MODEL=eng TESSDATA=../tesseract/tessdata MAX_ITERATIONS=100
```

To test the model just type in a terminal in tesstrain folder: 

```
tesseract data/Apex-ground-truth/eng_1.tif stdout --tessdata-dir /home/sharedFolder/trainingTest/tesstrain/data/ --psm 7 -l Apex --loglevel ALL
```

## Stop Image and destroy
Then to stop and delete container simply type:

```
docker compose down
```

If you wish to delete also the image, add ```--rmi 'all'``` to the command.

However if you just want to stop the container run:

```
docker compose stop
```

And then, to run it again type:

```
docker compose start
```

