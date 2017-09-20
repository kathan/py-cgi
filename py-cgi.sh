export PATH=/opt/local/bin:/opt/local/sbin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/opt/X11/bin

SCRIPT_FOLDER=`dirname $0`
cd "$SCRIPT_FOLDER"

gunicorn -b :8091 -w 24 -k gevent --worker-connections=2000 --backlog=1000 -p gunicorn.pid py-cgi:app 2>&1