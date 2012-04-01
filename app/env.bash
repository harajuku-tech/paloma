#!/bin/bash
PORT=9000
RUN()
{
    python manage.py runserver 0.0.0.0:$PORT
}
