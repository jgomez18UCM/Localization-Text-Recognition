FROM python:3.11.1-bullseye


WORKDIR /usr/app/src

COPY print.py ./

# CMD ["python3", "./print.py"]
