# jira-gitlab-relations

Add Issue in Jira Project <-> Add branch in Gitlab Project

## Install

```
pip3 install -r /app/requirements.txt
```

## Usage:

```
jira-gitlab-runner.py [-h] [--conf [CONF]] [--review] [--test]
```
* *--review* - review config;
* *--conf* - config file;
* *--test* - test program;
* *-h* - help;

## Config

### [PROGRAM]

* **METHOD** - server or service;
* **HOST** - listen server's IP-address;
* **PORT** - listen server's port.

### [GIT]

* **METHOD** - gitlab api method **OATH** or **TOKEN**;
* **URL** - gitlab api url;
* **USER** - username if **OATH** method;
* **PASS** - password if **OATH** method;
* **TOKEN** - private token if **TOKEN** method.

### [JIRA]

* **URL** - jira api url;
* **USER** - jira username;
* **PASS** - jira password;
* **ISSUE_TYPE** - filter issue type.

### [RELATIONS]

\<JIRA Project\>=\<Gitlab path\>

Example:

TEST=root/test

## JIRA

1. In Jira add webhook https://developer.atlassian.com/server/jira/platform/webhooks/

2. Add Jira project

3. Add issue type named "option" in project

## GitLab

1. Add GitLab project

2. Add "template" branch in GitLab Project

## Run 

1. Add Relation in config

2. Run server

```
./jira-gitlab-runner.py
```
