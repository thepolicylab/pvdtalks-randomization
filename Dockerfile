FROM python:3.7.3
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV FLASK_APP=autoapp.py

WORKDIR /app
COPY . ./
RUN pip install --no-cache-dir -r requirements.txt && pip install -e .