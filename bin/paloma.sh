#!/bin/sh -e

# Start or stop Paloma
#
# Hideki Nara <gmail@hdknr.com>
# based on Postfix's init.d script

### BEGIN INIT INFO
# Provides:          Paloma mailing manager
# Required-Start:    postfix
# Required-Stop:     
# Should-Start:      
# Should-Stop:       
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: start and stop the Paloma Mailing Manager
# Description:       paloma is mailing manager
### END INIT INFO

### Configure your environment 
#
DAEMON=/home/hdknr/ve/tact/bin/paloma_worker.py
USER=hdknr
NAME=paloma
PROJECTS="/home/hdknr/ve/tact/src/paloma/example/app\
         "
####

RUN=$1

test -x $DAEMON || exit 0
id $USER > /dev/null 2>&1 || exit 0

case $RUN in
    'install' ) insserv $NAME;;
    'uninstall') insserv -r $NAME;;
    ''|'start'|'stop') echo "running command";
        for PRJ in $PROJECTS; do
            (sudo -u $USER $DAEMON $PRJ $RUN)& 
        done
    ;;
esac

