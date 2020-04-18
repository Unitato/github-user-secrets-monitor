#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
REPO="github-user-secrets-monitor"
echo "Working in $DIR"
echo "Cleaning up $DIR/log/"
rm -rf $DIR/logs/*
docker build . -t $REPO
echo ""
LOAD_MOUNTS="-v $DIR/config/secrets.yaml:/app/config/secrets.yaml -v $DIR/logs:/app/log"
#LOAD_SECRETS="" #comment out if you want to load secrets
if [ "$1" == "bash" ]; then
  START="bash"
else
  START="python /app/main.py"
fi
docker run -it --rm $LOAD_MOUNTS $REPO $START


#cat logs/*
