# Manually run 'source venv/bin/activate' before running this make file
# make create (sh)
# make publish (zsh)

SUBDIRS := $(wildcard target/*)
NEW_TARGETS = $(patsubst %, %/target, $(SUBDIRS))

.PHONY: all
all: create

.PHONY: publish
publish: $(NEW_TARGETS)
	@echo $(SUBDIRS)
	@echo $(NEW_TARGETS)

# Target to create a virtual environment if it doesn't exist
venv:
	python3 -m venv venv

# Target to install dependencies
install: venv
	source venv/bin/activate; pip install -r requirements.txt

# Target to run the Python script
create: venv
	python3 src/crawler.py

$(NEW_TARGETS):
	@echo "XXXXXXXX"
	if [ $@ = target/README.md/target ]; then echo "Skip README.md"  ; \
	else \
	$(MAKE) -C $(subst /target,,$@)   &&\
	$(MAKE) load_data -C $(subst /target,,$@) \
	; fi

# Clean the project
.PHONY: clean
clean:
	rm -rf venv
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -rf {} +