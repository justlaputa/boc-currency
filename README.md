# boc-currency

## How to run at local

### use python 3 virtual env

```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

then you can run the scrapy command in local

```bash
# inspect a site
$ scrapy shell https://xxxxxx

# run crawler in local
$ scrapy crawl myspider
```

## Deploy

build the docker image by cloudbuild, then deploy with cloud-run:
```bash
make build-crawler
make deploy-crawler
```