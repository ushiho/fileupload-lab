FROM alpine:3.7
RUN apk update --no-cache && apk add python3 python3-dev py3-pip bash
COPY . /lab
WORKDIR /lab
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
CMD [ "python3", "app/server.py" ]
