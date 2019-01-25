#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        raw_request = str(self.data).split(' ')

        method = raw_request[0].split("\'")[1]
        request = raw_request[1]
        response = ''

        if (method == 'GET'):

            try:
                header = 'HTTP/1.1 200 OK\n'

                if request[-1] == "/":
                    request = str(request) + "index.html"
                
                #handle 301 redirect
                if (os.path.isdir("www/" + request) == True and request[-1] != "/") or request[-2:] == "..":
                    header = 'HTTP/1.1 301 Moved Permanently\n'
                    location = str(request) + "/"
                    header += 'Location: ' + str(location) + '\n\n'
                    request = str(request) + "/index.html"
                    file = open(("www/" + request), 'rb')
                    response = file.read()
                    file.close()
                    final_response = header.encode('utf-8')
                    if response != '':
                        final_response += response
                    self.request.sendall(final_response)
                    return

                file = open(("www/" + request), 'rb')

                server_dir = os.getcwd()
                abs_file_path = os.path.dirname(os.path.realpath(file.name))
                if abs_file_path.startswith(server_dir) == True:
                    response = file.read()
                    file.close()

                if request.endswith(".css"):
                    mimetype = 'text/css'
                elif request.endswith(".html"):
                    mimetype = 'text/html'

                header += 'Content-Type: ' + str(mimetype)+'\n\n'

            except:
                header = 'HTTP/1.1 404 Not Found\n\n'
                response = '<html><body><center><h3>Error 404: Not Found</h3><p>Raise your Truongers xd</p></center></body></html>'.encode('utf-8')

        else:
            header = 'HTTP/1.1 405 Not Allowed\n\n'
            response = '<html><body><center><h3>Error 405: Method Not Allowed</h3><p>Raise your Truongers xd</p></center></body></html>'.encode('utf-8')

        final_response = header.encode('utf-8')
        if response != '':
            final_response += response
        self.request.sendall(final_response)


# self.request.sendall(bytearray("OK",'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
