PROJECT_NAME=kset
MANAGE=python manage.py
SETTINGS=--settings=$(PROJECT_NAME).settings.test

DATA_DIR="__data"
DOCKER_POSTGRES_REPO=denibertovic/postgres
DOCKER_POSTGRES_TAG=9.3
PORT=5432


.PHONY: all test coverage clean requirements requirements-dev setup-test \
	docker-check db db-data-dir db-db db-user db-user-grant db-restore db-prompt

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
	python manage.py compilemessages
	python manage.py syncdb
	python manage.py migrate
	echo "Now run: python manage.py runserver and visit http://localhost:8000/"

update:
		git pull
		$(MAKE) clean
		$(MAKE) requirements
		python manage.py syncdb --noinput
		python manage.py migrate --noinput
		python manage.py collectstatic --noinput
		python manage.py compilemessages

deploy: update
		sudo supervisorctl restart $(PROJECT_NAME)-org

lint:
	flake8 --exclude=.git,migrations --max-complexity=10 .

docker-check:
	@command -v docker >/dev/null 2>&1 || \
		{ echo >&2 "Docker needs to be installed and on your PATH.  Aborting."; exit 1; }

db-data-dir: docker-check
	@if [ ! -d $(DATA_DIR)/postgresql ]; then \
		echo 'Preparing Postgres persistent data storage...'; \
		mkdir -p $(DATA_DIR); \
		chmod 777 $(DATA_DIR); \
		docker run --rm -v $$PWD/$(DATA_DIR):/tmp/$(DATA_DIR) -t \
			$(DOCKER_POSTGRES_REPO):$(DOCKER_POSTGRES_TAG)\
			/bin/bash -c "cp -rp var/lib/postgresql /tmp/$(DATA_DIR)"; \
	fi

db-prompt: db-data-dir
	@echo "Starting interactive database prompt (current dir mounted to /tmp/codebase)...";
	@docker run --rm -v $$PWD/$(DATA_DIR)/postgresql:/var/lib/postgresql -v $$PWD:/tmp/codebase -i -t \
		$(DOCKER_POSTGRES_REPO):$(DOCKER_POSTGRES_TAG) /bin/bash -c "/etc/init.d/postgresql start && psql -Upostgres";

db-db: db-data-dir
	@echo "Creating database...";
	@docker run --rm -v $$PWD/$(DATA_DIR)/postgresql:/var/lib/postgresql -t \
		$(DOCKER_POSTGRES_REPO):$(DOCKER_POSTGRES_TAG) /bin/bash -c "/etc/init.d/postgresql start && psql -Upostgres -c'CREATE DATABASE ksetdb;'";

db-user: db-data-dir
	@echo "Creating user..";
	@docker run --rm -v $$PWD/$(DATA_DIR)/postgresql:/var/lib/postgresql -t\
		$(DOCKER_POSTGRES_REPO):$(DOCKER_POSTGRES_TAG) /bin/bash -c "/etc/init.d/postgresql start && psql -Upostgres -c\"CREATE USER kset WITH SUPERUSER PASSWORD 'kset';\"";

db-user-grant: db-user
	@echo "Granting user required permissions...";
	@docker run --rm -v $$PWD/$(DATA_DIR)/postgresql:/var/lib/postgresql -t\
		$(DOCKER_POSTGRES_REPO):$(DOCKER_POSTGRES_TAG) /bin/bash -c "/etc/init.d/postgresql start && psql -Upostgres -c\"GRANT ALL ON DATABASE ksetdb to kset;\"";

db-restore: db-data-dir
	@if [ ! -f ksetdb.sql ]; then \
		echo "Aborting! Can't find backup file. Database backup file must be named ksetdb.sql and located in the current directory!"; \
		exit 1; \
	fi
	@echo "Restoring database from backup file: ksetdb.sql"
	@docker run --rm -v $$PWD/$(DATA_DIR)/postgresql:/var/lib/postgresql -v $$PWD:/tmp/codebase -i -t\
		$(DOCKER_POSTGRES_REPO):$(DOCKER_POSTGRES_TAG) /bin/bash -c "/etc/init.d/postgresql start && psql -Upostgres ksetdb < /tmp/codebase/ksetdb.sql";

db: db-db db-user-grant

