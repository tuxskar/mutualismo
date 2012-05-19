PIP=pip
PIPFLAGS=-r
PIP_REQUIREMENTS=requirements/base.txt
PIP_DEV_REQUIREMENTS=requirements/dev.txt

MANAGE=python manage.py
MANAGE_FLAGS=--noinput

bootstrap: base dev
	$(MANAGE) syncdb $(MANAGE_FLAGS) 
	$(MANAGE) migrate $(MANAGE_FLAGS) 
	$(MANAGE) rebuild_index $(MANAGE_FLAGS) 

base:
	$(PIP) install $(PIPFLAGS) $(PIP_REQUIREMENTS)

dev:
	$(PIP) install $(PIPFLAGS) $(PIP_DEV_REQUIREMENTS)

test:
	$(MANAGE) test red
