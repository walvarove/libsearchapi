#!/usr/bin/env bash
docker build -t fastapi_image .
docker run -d --name fastapi_container -p 80:80 fastapi_image