#!/usr/bin/env python3

port = 8008
ssl_enable = True

from socket import gethostname
from sys import argv, stdout, stderr, exit
from os import fstat
import os.path
argc = len( argv )

pathname_prefix = os.path.join(
        os.path.dirname(argv[ 0 ]),
        'myca', 'for_your_server', gethostname() )

ssl_keyfile = pathname_prefix + '.key'
ssl_certfile = pathname_prefix + '.crt'

helpmsg_to = argc > 1 and stderr or None

if argc == 2:

    argv1 = argv[ 1 ]

    if argv1 == '--help':

        helpmsg_to = stdout

    elif argv1 == '--plaintext':

        ssl_enable = False
        helpmsg_to = None

    else:
        try:

            port = int(argv1)
            helpmsg_to = None

        except ValueError: pass

elif argc == 3:

    ssl_keyfile, ssl_certfile = argv[ 2 ], argv[ 1 ]
    helpmsg_to = None

elif argc == 4:

    port, ssl_keyfile, ssl_certfile = int( argv1 ),  argv[ 2 ], argv[ 1 ]
    helpmsg_to = None

if helpmsg_to:

    helpmsg_to.write('\nUsage:\n'
        '\twebserver.py --help|--plaintext|[<port>][<cert-file> <key-file>]\n\n')

    exit( helpmsg_to is stderr and 1 or 0 )


from http.server import HTTPServer, SimpleHTTPRequestHandler

class RequestHandler( SimpleHTTPRequestHandler ):
    """
        from https://gist.github.com/mkows/cd2122f427ea722bf41aa169ef762001
    """
    def send_head(self):
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            if not self.path.endswith('/'):
                # redirect browser - doing basically what apache does
                self.send_response(301)
                self.send_header("Location", self.path + "/")
                self.end_headers()
                return None
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        ctype = self.guess_type(path)
        try:
            # Always read in binary mode. Opening files in text mode may cause
            # newline translations, making the actual size of the content
            # transmitted *less* than the content-length!
            f = open(path, 'rb')
        except IOError:
            self.send_error(404, "File not found")
            return None
        self.send_response(200)
        self.send_header("Content-type", ctype)
        fs = fstat(f.fileno())
        self.send_header("Content-Length", str(fs[ 6 ]))
        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp");
        self.send_header('Cross-Origin-Opener-Policy', "same-origin");

        self.end_headers()
        return f

httpd = HTTPServer( ('0.0.0.0', port), RequestHandler )

if ssl_enable:

    from ssl import SSLContext, PROTOCOL_TLS_SERVER

    ctx=SSLContext( PROTOCOL_TLS_SERVER )
    ctx.check_hostname = False
    ctx.load_cert_chain( keyfile= ssl_keyfile, certfile= ssl_certfile )
    httpd.socket = ctx.wrap_socket( httpd.socket, server_side= True )

stdout.write( "\nServing HTTP%s requests at any IP address on port %d.\n\n" %
        (ssl_enable and 'S' or '', port) )
httpd.serve_forever()

