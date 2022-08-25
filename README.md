Web Development Survival Kit
============================

`./myca/setup_*.sh`
-------------------

Scripts to create and run our own certificate authority which will provide appropriately signed SSL-keys. That is, browsers (by key-import) told to trust the CA will not complain about a security risk accessing an HTTPS host using keys properly matching its name.

`./web-server.py`
-----------------

Simple, Python-based, SSL-enabled web server script

The web server sets `Access-Control-Allow-Origin: *` and COEP/COOP response headers for cross-origin isolation.


