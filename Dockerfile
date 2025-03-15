FROM ubuntu:latest
LABEL authors="Tudor"
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv libpq-dev
WORKDIR /app
RUN python3 -m venv venv
COPY requirements.txt requirements.txt
RUN /bin/bash -c "source venv/bin/activate && pip install --no-cache-dir -r requirements.txt"
COPY . .
EXPOSE 5000
ENV FLASK_APP=app.py
CMD ["/bin/bash", "-c", "source venv/bin/activate && flask run --host=0.0.0.0"]