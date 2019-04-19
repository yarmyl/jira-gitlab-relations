# jira-gitlab

Add Issue in Jira Project -> Add branch in Gitlab Project

## Install

```
pip3 install -r /app/requirements.txt
```

## Usage:

```
jira-gitlab-runner.py [-h] [--conf [CONF]] [--review] [--test] [--webhook] [--puller]
```
* *--review* - review config;
* *--conf* - config file;
* *--test* - test program;
* *-h* - help;
* *--webhook* - WebHook server;
or
* *--puller* - Puller service.

## Config

### [SERVER]

* **HOST** - listen IP-address;
* **PORT** - listen port;

### [GIT]

* **METHOD** - gitlab api method **OATH** or **TOKEN**;
* **URL** - gitlab api url;
* **USER** - username if **OATH** method;
* **PASS** - password if **OATH** method;
* **TOKEN** - private token if **TOKEN** method.

### [RELATIONS]

\<JIRA Project\>=\<Gitlab path\>

Example:

TEST=root/test

## [JIRA]

1. In Jira add webhook https://developer.atlassian.com/server/jira/platform/webhooks/

2. Add Jira project

## [GitLab]

1. Add GitLab project

2. Add "template" branch in GitLab Project

## Run 

1. Add Relation in config

2. Run server

```
./jira-gitlab-runner.py
```
