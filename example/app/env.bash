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

DJDB()
{
    python ../manage.py dbshell
}

DJDUMP_PALOMA()
{
    python ../manage.py dumpdata --indent=2 $1  > ../../src/paloma/fixtures/$2/$1.json
}


TESTMAIL()
{
    python ../manage.py mail send --file ../../src/paloma/fixtures/test.eml
}
CI_LOG()
{
    tail -f /var/celery.log | grep -v djcelery_periodictasks
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
