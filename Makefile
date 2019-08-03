CRAWLER_IMAGENAME = gcr.io/laputa/currency-tracker
CHART_UPDATER_IMAGENAME = gcr.io/laputa/chart-updater
ENVS = $(shell cat .env | tr '\n' ',')

.PHONY: gcloud-build deploy

build-crawler:
	gcloud builds submit --project laputa --tag $(CRAWLER_IMAGENAME)

build-chart-updater:
	gcloud builds submit --project laputa --config chart-cloudbuild.yaml .

deploy-crawler:
	gcloud beta run \
		deploy currency-tracker \
		--region us-central1 \
		--platform managed \
		--service-account currency-tracker@personal-finance-228402.iam.gserviceaccount.com \
		--image $(CRAWLER_IMAGENAME) \
		--project personal-finance-228402

deploy-chart-updater:
	gcloud beta run \
		deploy chart-updater \
		--region us-central1 \
		--platform managed \
		--service-account currency-tracker@personal-finance-228402.iam.gserviceaccount.com \
		--set-env-vars $(ENVS) \
		--image $(CHART_UPDATER_IMAGENAME) \
		--project personal-finance-228402
