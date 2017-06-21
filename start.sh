#!/bin/sh
nohup python /app/python-greeter-service/app.py &
nohup python /app/python-name-service/app.py &
python /app/python-hello-world/app.py
