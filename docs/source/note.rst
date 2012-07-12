======
Note
======

configure worker
=====================

run.py has configuration parameters for django-celery.
Define wrapper command argment to run django-celery propery

::

    (paloma)hdknr@cats:~/ve/paloma/src/paloma/example/app$ vi run.py


app.run
----------

app.run.configure is called by paloma_worker.py command.

.. automodule:: app.run
    :members:

runnsing celery worker
====================================

use  bin/paloma.sh which is a command wrapper for paloma_worker.py.

At first configure arguments in paloma.sh.

to run::

    paloma.sh start

to stop::

    paloma.sh stop


"start" and "stop" are command defined in run.py.


Run at when Debian Linux is booted.
=======================================

copy paloma.sh ::

    sudo cp paloma.sh /etc/init.d/paloma

Configure autostart::

    sudo /etc/inid.d/paloma install

Stop autostart ::

    sudo /etc/inid.d/paloma uninstall


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


