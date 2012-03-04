#!/bin/bash
source  $(dirname $0)/conf.bash
if [ ! -d $PALOMA/run ] ;then
    mkdir -p $PALOMA/run
fi 
if [ -f $PALOMA/run/.sleep ] ; then
    rm $PALOMA/run/.sleep 
fi
echo $PYTHON
LOG=$PALOMA/run/celeryd.log
mv $LOG $LOG.old
$PYTHON $PALOMA/app/manage.py celeryd --loglevel DEBUG --pidfile=$PALOMA/run/celery.pid --logfile=$LOG &
