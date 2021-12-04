# chromium-and-selenium-on-aws-lambda

## Requirements
- pyenv
- Python v3.7.9  
- Selenium v3.14
- Serverless Framework
- unzip command

## Setup
```sh
unzip layers.zip
```

Creating a selenium-on-aws-lambda-screenshots bucket on S3 for saving screenshots.

## Deploy
```sh
sls deploy -v
```

## Remove
```sh
sls remove -v
```
