# github-user-secrets-monitor
A dockerized way to monitor for secret in github repos

## Installation
Copy and edit config/secrets-sample.yaml -> config/secrets.yaml
```
bash deploy.sh
```

## configuration
This monitor comes with some default detection mechanism found under config/bad-patterns.txt

## whitelisting
If you wish to exclude specific repo/string/regex, please edit config/whitelist-patterns.txt
