BINARY = currency-tracker
IMAGENAME = gcr.io/laputa/currency-tracker

.PHONY: gcloud-build deploy

gcloud-build: $(SRC)
	gcloud builds submit --project laputa --tag $(IMAGENAME)

deploy:
	gcloud beta run \
		deploy currency-tracker \
		--region us-central1 \
		--platform managed \
		--service-account currency-tracker@personal-finance-228402.iam.gserviceaccount.com \
		--image $(IMAGENAME)
