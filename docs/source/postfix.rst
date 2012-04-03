========================
Postfix Configuration
========================

Paloma application initialization
================================================

Postfix MySQL virtual configutaiton of this sample uses the application database and tables.

- create MySQL database for the app.
- run syncdb

::

    $ python manage.py syncdb

- run migrate if required becase the sample app depends on :term:`south` migration tool.


/etc/postfix configuration files
========================================================

For quick, copy your original Postfix configuation to backup , ::

    -rw-r--r-- 1 root root 1239 2012-03-04 16:21 main.cf.dist
    -rw-r--r-- 1 root root 5301 2012-03-04 16:21 master.cf.dist

And create symlinks for {{SOURCE}}/postfix/\*.cf files and **virtual** directory  ::


    lrwxrwxrwx   1 root root    48 2012-04-01 10:24 main.cf -> /home/hdknr/ve/paloma/src/paloma/postfix/main.cf
    lrwxrwxrwx   1 root root    50 2012-04-01 10:24 master.cf -> /home/hdknr/ve/paloma/src/paloma/postfix/master.cf
    lrwxrwxrwx   1 root root    49 2012-04-01 10:41 virtual -> /home/hdknr/ve/paloma/src/paloma/postfix/virtual/


Edit master.cf
----------------------------

- change your paloma_bouncer.py script path


Edit virtual/mysql/ files
-----------------------------------------------

- change your database access infomation 


/etc/hosts
============

- Edit hosts files for main.cf to work.

::

    127.0.0.1       paloma localhost paloma.localhost paloma.deb


Add a Domain
=============

- Create a test domain. Use {{SOURCE}}/src/paloma/fixtures/ file or create one with Django Admin UI.

.. code-block:: javascript

    [
      {
        "pk": 1, 
        "model": "paloma.domain", 
        "fields": {
          "domain": "paloma.deb", 
          "description": "paloma", 
          "maxquota": null, 
          "quota": null, 
          "active": true, 
          "backupmx": null, 
          "transport": "paloma"
        }
      }
    ]

Send a test mail
==================

All mails to **paloma.deb** domain and other domain are captured by paloma_bouncer.py and saved in Journal model table.

send ::

    (paloma)hdknr@cats:~/ve/paloma/src/paloma/app$ echo `date` | mail -s "test1" user1@paloma.deb
    (paloma)hdknr@cats:~/ve/paloma/src/paloma/app$ echo `date` | mail -s "test2" user1@hdknr.deb         


mail log ::

    Apr  4 03:18:45 cats postfix/master[1804]: daemon started -- version 2.7.1, configuration /etc/postfix
    
    Apr  4 03:53:42 cats postfix/pickup[1810]: A31E2550A7: uid=2000 from=<hdknr>Apr  4 03:53:42 cats postfix/cleanup[3286]: A31E2550A7: message-id=<20120403185342.A31E2550A7@paloma.localhost>
    Apr  4 03:53:42 cats postfix/qmgr[1811]: A31E2550A7: from=<hdknr@paloma.localhost>, size=329, nrcpt=1 (queue active)
    Apr  4 03:53:43 cats postfix/pipe[3291]: A31E2550A7: to=<user1@paloma.deb>, relay=paloma, delay=1.4, delays=0.41/0.06/0/0.96, dsn=2.0.0, status=sent (delivered via paloma service)
    Apr  4 03:53:43 cats postfix/qmgr[1811]: A31E2550A7: removed
    Apr  4 03:53:52 cats postfix/pickup[1810]: DC11A550A7: uid=2000 from=<hdknr>
    Apr  4 03:53:52 cats postfix/cleanup[3286]: DC11A550A7: message-id=<20120403185352.DC11A550A7@paloma.localhost>
    Apr  4 03:53:52 cats postfix/qmgr[1811]: DC11A550A7: from=<hdknr@paloma.localhost>, size=328, nrcpt=1 (queue active)
    Apr  4 03:53:53 cats postfix/pipe[3307]: DC11A550A7: to=<user1@hdknr.deb>, relay=jail, delay=0.85, delays=0.02/0.03/0/0.8, dsn=2.0.0, status=sent (delivered via jail service)
    Apr  4 03:53:53 cats postfix/qmgr[1811]: DC11A550A7: removed

Journal ::

    >>> from paloma.models import Journal                                                                                                                    >>> print map(lambda j : (j.sender,j.receipient,j.is_jailed), Journal.objects.all() )                                                                        
    [(u'hdknr@paloma.localhost', u'user1@hdknr.deb', True), (u'hdknr@paloma.localhost', u'user1@paloma.deb', False)]
