#!/usr/bin/python

import sys, cgi, cgitb
from os import path, environ, getpid, rename
from shutil import copyfileobj

cgitb.enable()

if environ['REQUEST_METHOD'] == 'GET':

    message = ""

else:

    fileitem = cgi.FieldStorage()[ 'upload' ]

    if fileitem.value:

        output_directory = path.join(
                path.dirname( sys.argv[ 0 ] ), path.pardir, 'uploads' )

        temp_file_name = 'upload%x.part' % getpid()
        temp_file_path = path.join( output_directory, temp_file_name )
        copyfileobj( fileitem.file, open( temp_file_path, 'wb' ) )

        file_name = path.basename( fileitem.filename )
        rename( temp_file_path, path.join( output_directory, file_name ) )

        message = "The file '%s' was uploaded successfully" % file_name

    else:

        message = "No file was uploaded."


print('''Content-Type: text/html

<html>
    <body>
        <p>
            <form enctype="multipart/form-data" action="file-upload.py" method="post">

                <label for="upload">File:</label>
                <input id="upload" type="file" name="upload" />

                <input type="submit" value="Upload" />
            </form>
        </p>
        <p>
            %s
        </p>
    </body>
</html>
''' % message )

