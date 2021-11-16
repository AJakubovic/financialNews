build:
	docker build -t financialnews:latest .

# build-prod:
# 	$(MAKE) build options="--target production"

compose-start:
	docker-compose up --remove-orphans

compose-stop:
	docker-compose down --remove-orphans

compose-manage-py:
	docker-compose run --rm website python manage.py $(cmd)
