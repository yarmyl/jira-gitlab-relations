FROM alpine:latest

COPY config.conf /app/

COPY gitclass.py /app/

COPY jiraclass.py /app/

COPY jira-gitlab-runner.py /app/ 

COPY web_server.py /app/

COPY requirements.txt /app/

RUN apk add --no-cache python3 libffi-dev python3-dev openssl-dev build-base && \
    pip3 install --upgrade pip && \
    pip3 install -r /app/requirements.txt && \
    cd /app

WORKDIR /app/

CMD ["jira-gitlab-runner.py"]
