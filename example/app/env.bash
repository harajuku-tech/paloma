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

TESTMAIL()
{
    python ../manage.py mail send --file ../../src/paloma/fixtures/test.eml
}
CI_SCHEDULED()
{
    python ../manage.py celery inspect scheduled
}
CI_REVOKED()
{
    python ../manage.py celery inspect revoked
}
CI_RESTART()
{
    sudo /etc/init.d/paloma stop
    sleep 1
    sudo /etc/init.d/paloma start
}
