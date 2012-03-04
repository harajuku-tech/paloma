#!/bin/bash
source  $(dirname $0)/conf.bash

if [ ! -f $PALOMA/run/celery.pid ] ;  then
    if [ ! -f $PALOMA/run/.sleep ] ; then 
        echo "waking up celeryd...."
        $PYTHON $PALOMA/website/manage.py celeryd --loglevel info --pidfile=$PALOMA/run/celery.pid --logfile=$PALOMA/run/celeryd.log &
    else
        echo "not wake up because .sleep file is found."
    fi
else
    echo "celeryd has been waked up and running"
fi
