STAGE = dev  # this is the environment we deploy to

test:
	docker-compose -f local.yml run --rm app python -m pytest

build:
	docker-compose -f local.yml build

up:
	docker-compose -f local.yml up

deploy_lambda:
	pip3 install -r requirements/serverless.txt --target libs
	cd libs; zip -r9 ../function.zip .; cd ..
	zip -rg function.zip app
	zip -g function.zip handler.py
	aws lambda update-function-code --function-name employer-api-$(STAGE)-callback --zip-file fileb://function.zip

clean:
	rm -rf test-reports
	rm .coverage
