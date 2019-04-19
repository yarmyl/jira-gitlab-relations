#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gitlab
import requests


class Gitapi:

    def __init__(self, auth):
        if auth['method'] == "OATH":
            self.oath_auth(
                auth['url'],
                self.pass_auth(auth['url'], auth['user'], auth['pass'])
            )
        elif auth['method'] == "TOKEN":
            self.token_auth(auth['url'], auth['token'])

    def token_auth(self, url, token):
        self.gl = gitlab.Gitlab(url, private_token=token)
        self.url = url
        self.token = token
        self.gl.auth()

    def pass_auth(self, url, user, passwd):
        url += 'oauth/token' if url[-1] == '/' else '/oauth/token'
        data = 'grant_type=password&username=' + user + '&password=' + passwd
        r = requests.post(url, data=data)
        self.user = user
        self.passwd = passwd
        return r.json()['access_token']

    def oath_auth(self, url, token):
        self.gl = gitlab.Gitlab(url, oauth_token=token)
        self.url = url
        self.token = token
        self.gl.auth()

    def check_proj(self, proj):
        try:
            self.gl.projects.get(proj)
        except:
            return 0
        return 1

    def add_branch(self, input, ref='template'):
        try:
            project = self.gl.projects.get(input[0])
        except:
            return "Wrong project path " + input[0]
        try:
            branch = project.branches.get(input[1])
        except:
            pass
        else:
            return "Branch already exists " + input[1]
        try:
            project.branches.create({'branch': input[1], 'ref': ref})
        except:
            return "Error to create branch"
        return "Branch successfully created"
