#  coding: utf-8 
import socketserver

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
        self.data = self.data.decode("utf-8")
        self.data = self.data.splitlines()
        if self.data[0][:3] != "GET":
            self.notGet()
        else:
            self.get(self.data)
        self.request.sendall(bytearray("OK",'utf-8'))

    def notGet(self):
        self.response = "HTTP/1.1 405 Method Not Allowed\r\n"
        self.request.send(bytearray(self.response,'utf-8'))
        return

    def get(self, data):
        self.notRoot(data[0][4:7])
        if self.data[0].split(" ")[1][-1]=="/":
            self.fetchIndex(self.data[0].split(" ")[1])
        elif self.data[0].split(" ")[1][-4:]==".css":
            self.getCSS(self.data[0].split(" ")[1])
        elif self.data[0].split(" ")[1][-5:]==".html":
            self.getHTML(self.data[0].split(" ")[1])
        else:
            self.redirect(self.data[0].split(" ")[1])

    def getHTML(self, url):
        try:
            file = open("./www"+url)
            f = file.read()
            file.close()
        except:
            self.response = "HTTP/1.1 404 Not Found\r\n"
            self.request.send(bytearray(self.response, 'utf-8'))
            return
        self.response = f'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(f)}\r\n\r\n{f}'
        self.request.send(bytearray(self.response, 'utf-8'))
        return

    def fetchIndex(self, url):
        try:
            file = open("./www"+url+"index.html")
            f = file.read()
            file.close()
        except:
            self.response = "HTTP/1.1 404 Not Found\r\n"
            self.request.send(bytearray(self.response, 'utf-8'))
            return
        self.response = f'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(f)}\r\n\r\n{f}'
        self.request.send(bytearray(self.response, 'utf-8'))
        return
            
    def redirect(self, url):
        try:
            file = open("./www"+url+"/index.html")
            f = file.read()
            file.close()
        except:
            self.response = "HTTP/1.1 404 Not Found\r\n"
            self.request.send(bytearray(self.response, 'utf-8'))
            return
        self.response = f'HTTP/1.1 301 Moved Permanently\r\nLocation: {url}/\r\n'
        self.request.send(bytearray(self.response, 'utf-8'))
        return

    def notRoot(self, url):
        if url == "/..":
            self.response = "HTTP/1.1 404 Not Found\r\n"
            self.request.send(bytearray(self.response, 'utf-8'))
            return

    def getCSS(self, url):
        try:
            file = open("./www"+url)
            f = file.read()
            file.close()
        except:
            self.response = "HTTP/1.1 404 Not Found\r\n"
            self.request.send(bytearray(self.response, 'utf-8'))
            return
        self.response = f'HTTP/1.1 200 OK\r\nContent-Type: text/css\r\nContent-Length: {len(f)}\r\n\r\n{f}'
        self.request.send(bytearray(self.response, 'utf-8'))
        return

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
