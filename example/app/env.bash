#!/bin/bash
PORT=9000

DJRUN()
{
    python ../manage.py runserver 0.0.0.0:$PORT
}

DJSYNC()
{
    python ../manage.py syncdb
}
DJSHELL()
{
    python ../manage.py shell
}

DBSHELL()
{
    python ../manage.py dbshell
}
