======
Note
======

configure worker
=====================

::

    (paloma)hdknr@cats:~/ve/paloma/src/paloma$ vi bin/conf.bash 


specify your virutalenv absolute path to $VE.

runnsing celery worker
====================================


::

    ;(paloma)hdknr@cats:~/ve/paloma/src/paloma$ bin/start_celery.bash 
    ;/home/hdknr/ve/paloma/bin/python
    ;(paloma)hdknr@cats:~/ve/paloma/src/paloma$ /home/hdknr/ve/paloma/lib/python2.6/site-packages/djcelery/loaders.py:103: UserWarning: Using settings.DEBUG leads to a memory leak, never use this setting in production environments!
    ;  warnings.warn("Using settings.DEBUG leads to a memory leak, never "



stopping celery worker
==============================


::

    (paloma)hdknr@cats:~/ve/paloma/src/paloma$ bin/stop_celery.bash 
    .
    /home/hdknr/ve/paloma
    celeryd-multi v2.5.1
    > Stopping nodes...
            > celery.cats: TERM -> 19505

    (paloma)hdknr@cats:~/ve/paloma/src/paloma$ bin/stop_celery.bash 
    .
    /home/hdknr/ve/paloma
    celeryd-multi v2.5.1
    > celery.cats: DOWN


testing
==============================

a bogus message

::

    (paloma)hdknr@cats:~/ve/paloma/src/paloma/app$ cat /tmp/msg.txt 

    From: gmail@hoge.com
    To: hdknr@foooooo.deb
    Subject:Hello
    
    My First mail

send a bogus message

::

    (paloma)hdknr@cats:~/ve/paloma/src/paloma/app$ cat /tmp/msg.txt  | python manage.py mail --command=send


list postfix queue

::

    (paloma)hdknr@cats:~/ve/paloma/src/paloma/app$ python manage.py postfix --command=qlist

    5595554E34*    2310 Mon Mar  5 04:14:19  MAILER-DAEMON

delete message form postfix queue 

::

    (paloma)hdknr@cats:~/ve/paloma/src/paloma/app$ python manage.py postfix --command=delete --id=5595554E34

    postsuper: 5595554E34: removed
    postsuper: Deleted: 1 message


