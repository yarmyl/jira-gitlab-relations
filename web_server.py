#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.server
import json


class Server(http.server.BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
        self.return_error(403)

    def return_error(self, code):
        self.message = ''
        self.send_response(code)
        self.end_headers()

    def do_POST(self):
        try:
            ctype = self.headers.get('content-type').split(';')[0]
            length = int(self.headers.get('content-length'))
        except:
            self.return_error(400)
            return
        if ctype != 'application/json':
            self.return_error(400)
            return
        try:
            message = json.loads(self.rfile.read(length))
        except:
            self.return_error(400)
            return
        self._set_headers()
        self.message = message
