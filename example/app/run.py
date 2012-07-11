import os
import sys
#
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

APP_DIR=os.path.dirname(__file__)
LOG_FILE="/tmp/celery.log"
PID_FILE="/tmp/celery.pid"
NODE="celery"           #: celery = default node
LOG_LEVEL="DEBUG"

####
def configure(args):
    if len(args) < 3:
        return []

    if  args[2] == "start" :
        return [ args[0], "celeryd",
                "--loglevel" , LOG_LEVEL,
                "--pidfile" , PID_FILE, 
                "--logfile" , LOG_FILE 
            ]

    if  args[2] == "stop":
        return [ args[0],"celeryd_multi",
                 "stop",NODE,
                "--pidfile=%s" % PID_FILE, 
            ]
