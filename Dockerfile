FROM ubuntu:latest
LABEL authors="Tudor"
RUN apt-get update && apt-get install -y python3 python3-pip
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
ENV FLASK_APP=app.py
CMD ["flask", "run", "--host=0.0.0.0"]