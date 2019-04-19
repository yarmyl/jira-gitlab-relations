#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.server
import argparse
import configparser
import web_server
import gitclass
import re


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--conf', nargs='?')
    parser.add_argument('--review', action='store_true')
    parser.add_argument('--test', action='store_true')
    parser.add_argument('--webhook', action='store_true')
    parser.add_argument('--puller', action='store_true')
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


def parse_mess(mess, relations):
    proj, branch = ("", "")
    try:
        if mess['webhookEvent'] == 'jira:issue_created':
            proj = mess['issue']['fields']['project']['name']
            branch = mess['issue']['fields']['summary']
            if not re.match(
                r"[\wа-яА-Я\-\.\,\+\=\/\!\&\@\#\$\%\(\)\{\}\]\"\'\`\;\№]+$",
                branch
            ):
                out("Wrong branch name")
                proj, branch = ("", "")
            if not relations.get(proj.lower()):
                out("Haven't relation "+proj.lower())
                proj, branch = ("", "")
            else:
                proj = relations[proj.lower()]
        else:
            out("Wrong webhook event!")
    except:
        out("Message parse error!")
    return (proj, branch)


def review(settings):
    err = ""
    if settings.get('SERVER') and \
            settings.get('GIT') and \
            settings.get('RELATIONS'):
        if settings['SERVER'].get('host'):
            host = settings['SERVER'].get('host')
        else:
            host = ''
        if settings['SERVER'].get('port'):
            port = int(settings['SERVER'].get('port'))
        else:
            port = 1111
        if settings['GIT'].get('method') and settings['GIT'].get('url'):
            if settings['GIT']['method'] == 'OATH':
                if not (
                    settings['GIT'].get('user') and settings['GIT'].get('pass')
                ):
                    err = "Wrong git auth config!"
            elif settings['GIT']['method'] == 'TOKEN':
                if not settings['GIT'].get('token'):
                    err = "Wrong git auth config!"
            else:
                err = "Wrong method!"
        rel = settings['RELATIONS']
    else:
        err = "Wrong config!"
    return (host, port, err, rel)


def start_puller(host, port, git, test, rels):
    pass


def start_server(host, port, git, test, rels):
    Handler = web_server.Server
    try:
        gitapi = gitclass.Gitapi(git)
    except:
        raise SystemExit("Error git connection!")
    for rel in rels:
        if not gitapi.check_proj(rels[rel]):
            raise SystemExit("Bad relation, haven't project "+rel)
    if not test:
        with http.server.HTTPServer((host, port), Handler) as httpd:
            print("serving at port", port)
            while 1:
                request, client_address = httpd.get_request()
                mess = Handler(request, client_address, httpd).message
                request.close()
                if mess:
                    arr = parse_mess(mess, rels)
                    if arr[1] and arr[0]:
                        out(gitapi.add_branch(input=arr))
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
    host, port, err, rel = review(settings)
    run = start_server
    if namespace.webhook:
        run = start_server
    if namespace.puller:
        run = start_puller
    if err:
        raise SystemExit(err)
    if not namespace.review:
        run(host, port, settings['GIT'], namespace.test, rel)
    else:
        raise SystemExit("Good config!")


if __name__ == "__main__":
    main()
