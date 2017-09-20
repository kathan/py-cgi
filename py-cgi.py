# Darrel Kathan 9/19/2017
# requires: gevent, gunicorn

import os
import json
import sys
import datetime
import time

tz = time.timezone / 3600.0
from gevent import monkey
monkey.patch_all()


def app(environ, start_response):
    file_path = environ['HTTP_PATH_TRANSLATED']+environ['PATH_INFO']
    base = os.path.basename(file_path)
    mod_name, ext = os.path.splitext(base)
    dir = os.path.dirname(file_path)
    data = None
    resp = "200 OK"
    resp_head = []
    
    info(environ['REQUEST_METHOD'] +' '+file_path)
    sys.path.insert(0, dir)
    try:
        mod = __import__(mod_name)
        #if is_changed(mod_name):
        mod = reload(mod)

        data = mod.cgi(environ, resp_head)
    except Exception as ex:
        err_type = type(ex).__name__
        if err_type == "ImportError":
            resp = "404 Not Found"
            data = "Error: File not found "+file_path+"."
        else:
            resp = "500 Internal Server Error"
            data = "Error: "+err_type+" in "+file_path+"."

    resp_head.append(("Content-Length", str(len(data))))
    start_response(resp, resp_head)
    return iter([data])

def log(type, msg):
    #now = datetime.datetime.utcnow()
    now = datetime.datetime.now().isoformat()
    print '['+now+'] ['+str(os.getpid())+'] ['+type+'] ' + msg
    
def info(msg):
    log('INFO', msg)
