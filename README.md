# py-cgi  - Python CGI process manager
py-cgi is a Python CGI process manager, similar to php-fpm, for executing python scripts behind NGINX or Apache. Comes in handy if you want to run python along side PHP, node.js or if you don't want to write your own web server into your python application. This is similar to [js-cgi](https://github.com/kathan/js-cgi)

### Dependencies:
* gunicorn
* gevent

### Usage:
Add a directive to your `nginx.conf` file.
```
location ~ [^/]\.py(/|$) {
    proxy_connect_timeout            10000;
    proxy_send_timeout               10000;
    proxy_read_timeout               10000;
    send_timeout                     10000;
    client_body_timeout              10000;
    proxy_pass                       http://localhost:8091;
    proxy_set_header X-Real-IP       $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header Host            $http_host;
    proxy_set_header path_translated $document_root$fastcgi_path_info;
}
```

Once you configure and restart NGINX, you can start py-cgi.
```sh
gunicorn -b :8091 -w 4 -k gevent --worker-connections=2000 --backlog=1000 -p gunicorn.pid py-cgi:app
```
