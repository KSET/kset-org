PROJECT_NAME=kset
MANAGE=python manage.py
SETTINGS=--settings=$(PROJECT_NAME).settings.test

DOCKER_VERSION=0.7
DATA_DIR="__data"
POSTGRES_VERSION=9.1
PORT=5432


.PHONY: all test coverage clean requirements requirements-dev setup-test \
	docker-check docker-version postgres

all: coverage

test:
	$(MANAGE) test --where=. $(SETTINGS) --nocapture

coverage:
	$(MANAGE) test --where=. $(SETTINGS) \
		--with-coverage --with-xunit --cover-html  --cover-erase

clean:
	rm -rf .coverage cover nosetests.xml
	find . -name '*.pyc' -exec rm '{}' ';'

requirements-dev:
	@if [ -z $$VIRTUAL_ENV ]; then \
		echo "You should probably install stuff in virtualenv instead."; \
		exit 1; \
	else \
		pip install -r requirements/dev.txt; \
	fi

requirements:
	@if [ -z $$VIRTUAL_ENV ]; then \
		echo "You should probably install stuff in virtualenv instead."; \
		exit 1; \
	else \
		pip install -r requirements/prod.txt; \
	fi

setup-dev:
	@if [ -z $$VIRTUAL_ENV ]; then \
		echo "Please set up virtualenv first."; \
		exit 1; \
	fi
	$(MAKE) requirements-dev
	$(MAKE) test
	[ ! -f $(PROJECT_NAME)/settings/local.py ] && \
		echo 'from .dev import *' > $(PROJECT_NAME)/settings/local.py
	python manage.py syncdb
	python manage.py migrate
	echo "Now run: python manage.py runserver and visit http://localhost:8000/"

update:
		git pull
		$(MAKE) clean
		$(MAKE) requirements
		python manage.py migrate
		python manage.py collectstatic --noinput

deploy: update
		sudo supervisorctl restart $(PROJECT_NAME)-org

lint:
	flake8 --exclude=.git,migrations --max-complexity=10 .

docker-check:
	@command -v docker >/dev/null 2>&1 || \
		{ echo >&2 "Docker needs to be installed and on your PATH.  Aborting."; exit 1; }

docker-version: docker-check
	@if ! docker version | grep "Server version" | grep $(DOCKER_VERSION) > /dev/null; \
		then \
			echo "ERROR: Wrong docker version. Recommended version: $(DOCKER_VERSION)"; \
			exit 1; \
	fi

postgres: docker-version
	@if nmap -PS localhost | grep -q $(PORT); then \
		echo "ERROR: Port $(PORT) is already in use..."; \
		echo "Maybe Postgres is already running?!"; \
		exit 1; \
	fi
	@if [ ! -d $(DATA_DIR)/postgresql ]; then \
		echo 'Preparing Postgres persistent data storage...'; \
		mkdir -p $(DATA_DIR); \
		docker run -v $$PWD/$(DATA_DIR):/tmp/$(DATA_DIR) -i -t \
			denibertovic/postgres:$(POSTGRES_VERSION)\
			/bin/bash -c "cp -rp var/lib/postgresql /tmp/$(DATA_DIR)"; \
	fi
	@echo "Persistent data storage found.";
	@echo "Starting postgres...";
	@docker run -v $$PWD/$(DATA_DIR)/postgresql:/var/lib/postgresql -d -p $(PORT):$(PORT) \
		denibertovic/postgres:$(POSTGRES_VERSION) /usr/local/bin/start_postgres.sh;
