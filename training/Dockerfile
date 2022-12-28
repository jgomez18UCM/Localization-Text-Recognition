FROM python:3.11.1-bullseye

#NOTE: all of this commands are in https://tesseract-ocr.github.io/tessdoc/Compiling.html#windows and 
#https://tesseract-ocr.github.io/tessdoc/Compiling-%E2%80%93-GitInstallation.md

RUN apt-get update -y 
RUN apt-get install bc 
RUN apt-get install build-essential
RUN apt install unzip
RUN apt install zip

#Cloning Tesseract repositoreis
RUN mkdir /home/tesseract_repos
RUN git clone https://github.com/tesseract-ocr/tesseract     /home/tesseract_repos/tesseract
WORKDIR /home/tesseract_repos/tesseract
#Checking to tesseract version 5.2
RUN cd /home/tesseract_repos/tesseract
RUN git checkout 5.2.0

#Checking tesstrain working version
RUN git clone https://github.com/tesseract-ocr/tesstrain     /home/tesseract_repos/tesstrain
WORKDIR /home/tesseract_repos/tesstrain
RUN cd /home/tesseract_repos/tesstrain
RUN git checkout 43ff10012af31914bb5b72304d9c21c8fdf4f464
#Lenguage traineddata models
RUN git clone https://github.com/tesseract-ocr/tessdata_best /home/tesseract_repos/tessdata_best
#Training Text for lenguages
RUN git clone https://github.com/tesseract-ocr/langdata_lstm /home/tesseract_repos/langdata_lstm

        
#Tesseract dependencies
RUN apt-get install g++ # or clang++ (presumably) -y
RUN apt-get install autoconf automake libtool -y
RUN apt-get install pkg-config -y
RUN apt-get install libpng-dev -y
RUN apt-get install libjpeg62-turbo-dev -y
RUN apt-get install libtiff5-dev -y
RUN apt-get install zlib1g-dev -y
RUN apt-get install libicu-dev -y
RUN apt-get install libpango1.0-dev -y
RUN apt-get install libcairo2-dev -y 
RUN apt-get install libleptonica-dev -y

#use lscpu | egrep 'Model name|Socket|Thread|NUMA|CPU\(s\)' to get number of threads and use them all in MAKE commands. 
#or if you're using Windows, go to task Manager, Performance tab and the Logical Processors field  indicates number of threads. 
#In my case I have, 6 cores which means 12 threads. 

RUN  ./autogen.sh
RUN  ./configure --disable-debug 'CXXFLAGS=-g -O3'

#Bulding tesseract
RUN make -j12
RUN make install
RUN ldconfig
RUN make training-install -j12
RUN tesseract -v

#TODO DELETE AFTER GETTING TRAINED
RUN git clone https://github.com/astutejoe/tesseract_tutorial /home/trainingTest

RUN git clone https://github.com/tesseract-ocr/tesseract     /home/trainingTest/tesseract
WORKDIR /home/trainingTest/tesseract
RUN cd /home/trainingTest/tesseract
RUN git checkout 5.2.0

RUN git clone https://github.com/tesseract-ocr/tesstrain     /home/trainingTest/tesstrain
WORKDIR /home/trainingTest/tesstrain
RUN cd /home/trainingTest/tesstrain
RUN git checkout 43ff10012af31914bb5b72304d9c21c8fdf4f464

WORKDIR /home

#TODO UNCOMMENT
# COPY create-ground-truth .

