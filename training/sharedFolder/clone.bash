#!/bin/bash
#(mkdir /home/sharedFolder/prueba ; git clone https://github.com/tesseract-ocr/tesstrain  /home/sharedFolder/prueba & ; cd /home/sharedFolder/prueba/ ) &

# bash -c " mkdir /home/sharedFolder/prueba ; \ 
#         git clone https://github.com/tesseract-ocr/tesseract  /home/sharedFolder/prueba/tesseract ; \
#         cd /home/sharedFolder/prueba/tesseract ; \ 
#         git checkout 5.2.0 || \
#         echo Failed to clone respository ;
#         cd .." \
#         &>/dev/null &



# bash -c "git clone https://github.com/tesseract-ocr/tesstrain  /home/sharedFolder/prueba/tessTrain ; \
#         cd /home/sharedFolder/prueba/tessTrain ; \ 
#         git checkout 43ff10012af31914bb5b72304d9c21c8fdf4f464 || \
#         echo Failed to clone respository " \
#         &>/dev/null &

bash -c "git clone https://github.com/tesseract-ocr/tessdata_best /home/sharedFolder/prueba/tessdata_best" &>/dev/null &