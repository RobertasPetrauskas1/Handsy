# Handsy
University project to learn SOA and Python with FastAPI

## Local setup
1. Clone this repo
2. Build the docker image with `docker build . -t saitynai`
3. Run the image with `docker run -p 80:80 --name saitynai`

## Deployment
Deployment is done on azure cloud. Workflow is automated using Github Actions. All pushes to master branch are automaticaly redeployed to azure.

Live api docs can be found [here](http://saitynai-cd.azurewebsites.net/docs)
