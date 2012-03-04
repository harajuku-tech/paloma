export APP_DB=nr_sitecast
VE=/home/hdknr/ve/paloma
PYTHON=$VE/bin/python
if [ $(dirname $0) == '.' ]; then
    PALOMA=..
else
    PALOMA=$(dirname $(dirname $0))
fi
NODE=celery
