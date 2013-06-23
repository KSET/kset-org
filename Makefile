PROJECT_NAME=kset
MANAGE=python manage.py
SETTINGS=--settings=$(PROJECT_NAME).settings.test
LESS_PATH="utils/static/less"


.PHONY: all test coverage clean requirements requirements-dev setup-test css

all: coverage

test:
	$(MANAGE) test --where=. --processes=4 $(SETTINGS)

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
	python manage.py syncdb --all
	python manage.py migrate --fake
	echo "Now run: python manage.py runserver and visit http://localhost:8000/"

deploy: css
		git pull
		$(MAKE) requirements
		python manage.py migrate
		python manage.py collectstatic --noinput


css:
		for f in $(LESS_PATH)/*.less ; do \
		  fname=$${f##*/}; \
		  lessc $$f utils/static/css/"$${fname%.less}.css" ; \
		done

restart: deploy
		sudo restart $(PROJECT_NAME)-web

lint:
	flake8 --exclude=.git,migrations --max-complexity=10 .
