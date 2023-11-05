# docker build -t animeita:latest .
# docker run animeita:latest
FROM python:latest
LABEL maintainer="feltrin.gi@gmail.com"

WORKDIR /usr/src/app

COPY /kodi20/chobe/animeita.py ./
COPY /kodi20/chobe/resources ./
#COPY requirements.txt
#RUN pip install -r requirements.txt
RUN pip install requests
RUN pip install beautifulsoup4

CMD [ "python", "./animeita.py" ]