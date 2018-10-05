from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import threading
import json
import ssl
import os

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Mock API Server')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        # data = json.loads(body)
        # data["message"] = "%s from API server " % data["message"]
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        # response.write(json.dumps(data))
        self.wfile.write(response.getvalue())

def main():
    httpd = HTTPServer(('', 8183), SimpleHTTPRequestHandler)

    if int(os.environ["USE_SSL"]):
        httpd.socket = ssl.wrap_socket (httpd.socket,
            keyfile="key.pem",
            certfile='cert.pem', server_side=True)

    print ("API Mock server starting...")

    threading.Thread(target=httpd.serve_forever).start()

if __name__ == '__main__':
    main()



