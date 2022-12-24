FROM jitesoft/tesseract-ocr


RUN mkdir /tmp/images
RUN train-lang bul --fast
