paloma
========================================================================

under development.

django-celery
------------------

install
^^^^^^^^^^^^^^^^^^

::

   $  pip install django-celery --upgrade

MySQL for queue engine
^^^^^^^^^^^^^^^^^^^^^^^^^^^

settins.py::

    INSTALLED_APPS += ('djcelery','djkombu',) 
    import djcelery 
    djcelery.setup_loader() 
    BROKER_URL="django://" 

InnoDB ? Lock down the transaction isolation level to COMMIT READ 
( form MySQL default REPEATABLE READ )

::

    (paloma)hdknr@sqg:~$ sudo vi /etc/mysql/my.cnf 


    [mysqld]
    transaction-isolation = READ-COMMITTED


    (paloma)hdknr@sqg:~$ sudo /etc/init.d/mysql restart
    Stopping MySQL database server: mysqld
    .
    Starting MySQL database server: mysqld . . . . . . ..
    Checking for corrupt, not cleanly closed and upgrade needing tables..


tools
--------

- mandb

    - ssh://hg@bitbucket.org/hdknr/mandb

south
---------

celery needs the following talbe. "syncdb" DON'T create those with "south". 
First time syncdb without "south".

::

    Creating table celery_taskmeta
    Creating table celery_tasksetmeta
    Creating table djcelery_intervalschedule
    Creating table djcelery_crontabschedule
    Creating table djcelery_periodictasks
    Creating table djcelery_periodictask
    Creating table djcelery_workerstate
    Creating table djcelery_taskstate
    
