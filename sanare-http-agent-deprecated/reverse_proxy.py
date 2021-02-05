#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import argparse
from pymongo import MongoClient
import sys
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)




#hostname = 'en.wikipedia.org'
hostname = '10.1.0.100:8000'
client = MongoClient('10.1.0.101', 27017)
db = client.sanare


def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

def set_header():
    headers = {
        'Host': hostname
    }

    return headers

class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.0'
    def do_HEAD(self):
        self.do_GET(body=False)

    def do_GET(self, body=True):
        sent = False
        try:
            url = 'http://{}{}'.format(hostname, self.path)
            req_header = self.parse_headers()
            print(req_header)
            print(url)
            resp = requests.get(url) #-- tb funciona
            #resp = requests.get(url, headers=merge_two_dicts(req_header, set_header()), verify=False)
            sent = True
            self.send_response(resp.status_code)
            self.send_resp_headers(resp)

            httplogentry = {
                "url": url,
                "verb": "GET",
                "authenticated": False,
                "cookie": req_header["Cookie"],
                "client": self.address_string()
            }
            httplogentries = db.httplogentries
            httplogentry_id = httplogentries.insert_one(httplogentry).inserted_id
            print("New id = " + str(httplogentry_id))

            if body:
                try:
                    print(resp.content)
                    str_content = resp.content.decode("UTF-8")
                    str_content = str_content.replace("localhost:8000", "localhost:9999")
                    self.wfile.write(str_content.encode("UTF-8"))
                except:
                    self.wfile.write(resp.content)
            return
        finally:
            #self.finish()
            if not sent:
                self.send_error(404, 'error trying to proxy')

    def do_POST(self, body=True):
        sent = False
        try:
            url = 'http://{}{}'.format(hostname, self.path)
            content_len = int(self.headers.getheader('content-length', 0))
            post_body = self.rfile.read(content_len)
            req_header = self.parse_headers()

            resp = requests.post(url, data=post_body, headers=merge_two_dicts(req_header, set_header()), verify=False)
            sent = True

            self.send_response(resp.status_code)
            self.send_resp_headers(resp)
            if body:
                self.wfile.write(resp.content)
            return
        finally:
            self.finish()
            if not sent:
                self.send_error(404, 'error trying to proxy')

    def parse_headers(self):
        req_header = {}

        for key in self.headers.keys():
            req_header[key] = self.headers.get(key)
        return req_header

    def send_resp_headers(self, resp):
        respheaders = resp.headers
        print('Response Header')
        for key in respheaders:
            if key not in ['Content-Encoding', 'Transfer-Encoding', 'content-encoding', 'transfer-encoding', 'content-length', 'Content-Length']:
                #print (key)
                #print(respheaders[key])
                self.send_header(key, respheaders[key])
        self.send_header('Content-Length', len(resp.content))
        self.end_headers()



# def parse_args(argv=sys.argv[1:]):
#     parser = argparse.ArgumentParser(description='Proxy HTTP requests')
#     parser.add_argument('--port', dest='port', type=int, default=8080,
#                         help='serve HTTP requests on specified port (default: random)')
#     args = parser.parse_args(argv)
#     return args




# def main(argv=sys.argv[1:]):
#     args = parse_args(argv)



#     print('http server is starting on port {}...'.format(args.port))
#     server_address = ('127.0.0.1', args.port)
#     httpd = HTTPServer(server_address, ProxyHTTPRequestHandler)
#     print('http server is running as reverse proxy')
#     httpd.serve_forever()


# if __name__ == '__main__':
#     main()



def start_reverse_proxy(port):
    # args = parse_args(argv)
    # port = 8080


    print('http server is starting on port {}...'.format(port))
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, ProxyHTTPRequestHandler)
    print('http server is running as reverse proxy')
    httpd.serve_forever()