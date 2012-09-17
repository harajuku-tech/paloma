import os
import sys
#
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

APP_DIR=os.path.dirname(__file__)
LOG_FILE="/tmp/paloma.log"  #: celery worker logfile 
PID_FILE="/tmp/paloma.pid"  #: celery worker PID file
PID_CAM="/tmp/paloma.pid"
NODE="celery"           #: celery = default node
LOG_LEVEL="DEBUG"       #: celery log level

def configure(*args):
    ''' return django-celery parameter for specified args

        - args[0] : paloma_worker.py
        - args[1] : path this django project application 
        - args[2] : command
    '''

    if  len(args) < 3 or args[2] == "start" :
        #: start worker
        #: TODO: Check some exiting process
        return [ 
                "celery","worker",
                "--loglevel=%s" % LOG_LEVEL,
                "--pidfile=%s"  %  PID_FILE, 
                "--logfile=%s"  %  LOG_FILE ,
                "-E",            # event option for celerycam
                "--beat" , 
                "--scheduler=djcelery.schedulers.DatabaseScheduler",
            ]

    if  len(args) >2 and args[2] == "stop":
        #: stop worker
        return [
                "celery","multi",
                "stop",NODE,
                "--pidfile=%s" % PID_FILE, 
            ]

    if  len(args) >2 and args[2] == "cam":
        #: TODO: Check some exiting process
        return [
                 "celerycam",
                "--pidfile=%s" % PID_CAM, 
               ]

    if  len(args) >2 and args[2] == "camstop":
        #: TODO: Check some exiting process
        return [ 
                "celery","multi",
                "stop",NODE,
                "--pidfile=%s" % PID_CAM, 
            ]
