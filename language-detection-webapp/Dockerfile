FROM zironycho/jpype3

WORKDIR /usr/src/app

# openblas-dev and alpine-sdk (gcc) are required to build scipy
RUN apk add --no-cache git openblas-dev
RUN apk add --update alpine-sdk 

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD [ "python", "server.py", "--host", "0.0.0.0" ]
