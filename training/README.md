# <b>Running Tesseract Training Tools Image</b>
Before running the image, check the Dockerfile to ensure you have the same number of threads, or if different change the values from 12 to your
exact number of threads. The values are "12" in the "#Bulding tesseract" section.

### Pre-work 
Copy desired files to _sharedFolder_ in order to work with them inside container, and keep persistency so they don't get deleted when container shutsdown.

Moreover, copy desired fonts inside _fonts_ folder, so you can use them in the container. There is an Apex font as example.

## <u>Start Image and Run</u>
To run the container and docker image simply run Docker Desktop and type in a terminal inside _./training_ folder:

```
docker compose up -d
```

To get inside container just simply type:

```
.\connect.bat tesseract-cont
```

A short bat file that executes ``` docker exec -it tesseract-cont bash```


**NOTE: It could take around 10 min to build the image since it has to download and clone necessary dependencies and repositories.**

<!--- 
It clones everything at the same time so you can check if has finished using ```git status```  inside each repo folder in tesseract_repos.

- <b>tesseract</b> should show next message:

  <font color="red">HEAD detached at</font> 5.2.0 

- <b>tesstrain</b> should show next message:

  <font color="red">HEAD detached at</font> 43ff100 

- <b>langdata_lstm</b> should show next message:

  On branch main. Your branch is up to date with 'origin/main'.

  nothing to commit, working tree clean

- <b>tessdata_best</b> should show next message:

  On branch main. Your branch is up to date with 'origin/main'.

  nothing to commit, working tree clean

Otherwise, wait until those messages show up.
--->

## <u>Training</u>

If you haven't placed your font inside _fonts_ folder before creating this image, copy it in mentioned folder so you can use it inside container.

Copy custom font file inside _/usr/local/share/fonts_ and run the following command so the OS recognize the font.
```
fc-cache -f -v
```

Launch script trainOCR.py inside _trainingFont_ folder with following syntax:

``` 
python trainOCR.py [lenguaje] [fontName] [num max training iterations]
```

For instance, to train the example font Apex with an english lenguage, it should look like this:

``` 
python trainOCR.py eng Apex 200
```

**NOTE: The final trained model should be copied to _trainedModel_ inside _trainingFont_.**

<!---Copy desired lenguage traineddata to tesseract/tessdata/

Create ground-truth for desired custom font using python script.

Go to tesstrain and run with custom font and number of iterations (i.e we use Apex name font):

```
TESSDATA_PREFIX=../tesseract/tessdata make training MODEL_NAME=Apex START_MODEL=eng TESSDATA=../tesseract/tessdata MAX_ITERATIONS=100
```-->

If you get an error saying ***<span style="color:red;">bc: command not found</span>*** just run ```apt-get install bc``` and try again. 

To test the model just type in a terminal inside _tesstrain_ folder: 

```
tesseract data/Apex-ground-truth/eng_1.tif stdout --tessdata-dir /home/tesseract_repos/tesstrain/data/ --psm 7 -l Apex --loglevel ALL
```

## <u>Stop Image and destroy</u>
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

