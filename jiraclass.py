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
        if mess != "Error to create branch" or \
                mess[:18] != "Wrong project path":
            self.to_progress(issue)
        if mess == "Wrong branch name":
            self.to_reject(issue, '10001')
        elif mess[:21] == "Branch already exists":
            self.to_reject(issue, '10002')

    def check_proj(self, proj):
        try:
            self.jira.project(proj)
        except:
            return 0
        return 1

    def find_issues(self, keys):
        str = ""
        for key in keys:
            str += ' or project=' + key
        str = "(" + str[4:] + ") and issuetype='option' and status=open"
        return self.jira.search_issues(str)

    def to_progress(self, issue):
        return self.jira.transition_issue(issue, '11')

    def to_reject(self, issue, res):
        return self.jira.transition_issue(issue, '111', resolution={'id': res})
