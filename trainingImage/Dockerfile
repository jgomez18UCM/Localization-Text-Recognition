FROM python:3.11.1-bullseye

#tesseract dependencies
RUN     apt-get update -y\ 
        cd /home \
        git clone https://github.com/tesseract-ocr/tesseract -y\
        apt-get install g++ # or clang++ (presumably) -y\
        apt-get install autoconf automake libtool -y\
        apt-get install pkg-config -y\
        apt-get install libpng-dev -y\
        apt-get install libjpeg62-turbo-dev -y\
        apt-get install libtiff5-dev -y\
        apt-get install zlib1g-dev -y\
        apt-get install libicu-dev -y\
        apt-get install libpango1.0-dev -y\
        apt-get install libcairo2-dev -y \
        apt-get install libleptonica-dev -y

RUN cd /home/tesseract \
    git checkout 5.2.0

#use lscpu | egrep 'Model name|Socket|Thread|NUMA|CPU\(s\)' to get number of threads and use them all in make commands. In my case I have 12.

RUN  ./autogen.sh \
    ./configure --disable-debug 'CXXFLAGS=-g -O3'\
    make -j12 \
    make install \
    ldconfig \
    make training-install -j12 \
    tesseract -v

WORKDIR /usr/app/src

COPY print.py ./

# CMD ["python3", "./print.py"]
