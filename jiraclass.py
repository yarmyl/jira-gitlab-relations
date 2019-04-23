#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import jira


class Jirapi:

    def __init__(self, auth):
        self.pass_auth(auth['url'], auth['user'], auth['pass'])

    def pass_auth(self, url, user, passwd):
        self.jira = jira.JIRA(url, auth=(user, passwd))

    def out(self, mess, key):
        issue = self.jira.issue(key)
        self.jira.add_comment(issue, mess)