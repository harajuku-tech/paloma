#!/bin/bash
source  $(dirname $0)/conf.bash
echo $PALOMA
echo $VE
touch $PALOMA/run/.sleep
$PYTHON $PALOMA/app/manage.py celeryd_multi stop $NODE --pidfile=$PALOMA/run/celery.pid
