#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.server
import argparse
import configparser
import re
import time
import web_server
import gitclass
import jiraclass


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--conf', nargs='?')
    parser.add_argument('--review', action='store_true')
    parser.add_argument('--test', action='store_true')
    return parser


def out(mess):
    print(mess)


def get_settings(config):
    settings = dict()
    for section in config.sections():
        value = dict()
        for setting in config[section]:
            value.update({setting: config.get(section, setting)})
        settings.update({section: value})
    return settings


def check_name(name):
    if not re.match(
        r"[\w\-\.\,\+\=\/\!\&\@\#\$\%\(\)\{\}\"\'\`\;\№]+$",
        name
    ):
        return 1
    return 0


def parse_mess(mess, relations, itype):
    proj, branch, key, err = ("", "", "", "")
    try:
        if mess['webhookEvent'] == 'jira:issue_created':
            if not mess['issue']['fields']['issuetype']['name'] == itype:
                return ("", "", "", "Wrong Issue Type")
            else:
                proj = mess['issue']['fields']['project']['key']
                branch = mess['issue']['fields']['summary']
                key = mess['issue']['key']
                if check_name(branch):
                    return ("", "", key, "Wrong branch name")
                elif not relations.get(proj.lower()):
                    return ("", "", "", "Haven't relation "+proj.lower())
                else:
                    proj = relations[proj.lower()]
        else:
            return ("", "", "", "Wrong webhook event!")
    except:
        return ("", "", "", "Message parse error!")
    return (proj, branch, key, err)


def review(settings):
    if settings.get('PROGRAM') and \
            settings.get('GIT') and \
            settings.get('RELATIONS') and \
            settings.get('JIRA'):
        if settings['PROGRAM'].get('method') == "server":
            if settings['PROGRAM'].get('port') is None:
                return "Wrong server port config!"
            if settings['PROGRAM'].get('host') is None:
                return "Wrong server ip config!"
        elif settings['PROGRAM'].get('method') == "service":
            pass
        else:
            return "Wrong method config!"
        if settings['GIT'].get('method') and settings['GIT'].get('url'):
            if settings['GIT']['method'] == 'OATH':
                if not (
                    settings['GIT'].get('user') and settings['GIT'].get('pass')
                ):
                    return "Wrong git auth config!"
            elif settings['GIT']['method'] == 'TOKEN':
                if not settings['GIT'].get('token'):
                    return "Wrong git auth config!"
            else:
                return "Wrong method!"
        if not settings['JIRA'].get('issue_type'):
            return "Wrong Jira config"
        if not settings['JIRA'].get('url'):
            return "Wrong Jira config"
        if not settings['JIRA'].get('user'):
            return "Wrong Jira config"
        if not settings['JIRA'].get('pass'):
            return "Wrong Jira config"
        rel = settings['RELATIONS']
    else:
        return "Wrong config!"
    return ""


def start_puller(prog, git, jira, rels, test):
    keys = []
    try:
        gitapi = gitclass.Gitapi(git)
    except:
        raise SystemExit("Error git connection!")
    try:
        jirapi = jiraclass.Jirapi(jira)
    except AttributeError:
        raise SystemExit("Error jira connection!")
    for rel in rels:
        keys += [rel.upper()]
        if not gitapi.check_proj(rels[rel]):
            raise SystemExit("Bad relation, haven't project "+rel)
        if not jirapi.check_proj(rel.upper()):
            raise SystemExit("Bad relation, haven't project "+rel)
    if not test:
        while 1:
            issues = jirapi.find_issues(keys)
            if issues:
                for i in issues:
                    if check_name(i.fields.summary):
                        jirapi.out("Wrong branch name", i.key)
                    else:
                        jirapi.out(
                            gitapi.add_branch(
                                input=[
                                    rels[i.fields.project.key.lower()],
                                    i.fields.summary
                                ]
                            ),
                            i.key
                        )
            time.sleep(60)
    raise SystemExit("Good test config!")


def start_server(prog, git, jira, rels, test):
    Handler = web_server.Server
    try:
        gitapi = gitclass.Gitapi(git)
    except:
        raise SystemExit("Error git connection!")
    try:
        jirapi = jiraclass.Jirapi(jira)
    except AttributeError:
        raise SystemExit("Error jira connection!")
    for rel in rels:
        if not gitapi.check_proj(rels[rel]):
            raise SystemExit("Bad relation, haven't project "+rel)
    if not test:
        host = prog['host']
        port = int(prog['port'])
        with http.server.HTTPServer((host, port), Handler) as httpd:
            print("serving at port", port)
            while 1:
                request, client_address = httpd.get_request()
                mess = Handler(request, client_address, httpd).message
                request.close()
                if mess:
                    arr = parse_mess(mess, rels, jira['issue_type'])
                    if arr[1] and arr[0] and arr[2]:
                        jirapi.out(gitapi.add_branch(input=arr), arr[2])
                    elif arr[2] and arr[3]:
                        jirapi.out(arr[3], arr[2])
                    else:
                        out(arr[3])
            httpd.server_close()
    raise SystemExit("Good test config!")


def main():
    parser = createParser()
    namespace = parser.parse_args()
    parser = configparser.ConfigParser()
    if namespace.conf:
        parser.read(namespace.conf)
    else:
        parser.read('config.conf')
    settings = get_settings(parser)
    err = review(settings)
    run = start_server
    if settings['PROGRAM']['method'] == 'server':
        run = start_server
    elif settings['PROGRAM']['method'] == 'service':
        run = start_puller
    if err:
        raise SystemExit(err)
    if not namespace.review:
        run(
            settings['PROGRAM'],
            settings['GIT'],
            settings['JIRA'],
            settings['RELATIONS'],
            namespace.test
        )
    else:
        raise SystemExit("Good config!")


if __name__ == "__main__":
    main()
