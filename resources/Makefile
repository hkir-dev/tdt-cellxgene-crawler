
SUBDIRS := $(wildcard target/*)
INPUT_DATA = $(patsubst %, %/input_data/taxonomy.json, $(SUBDIRS))

.PHONY: all
all: run

run:
	./seed-via-docker.sh -C project_config.yaml

$(INPUT_DATA):
	cp taxonomy.json $@
	cd $(subst /input_data/taxonomy.json,,$@) && \
	git add ./input_data/taxonomy.json

load_data: $(INPUT_DATA)
	cd $(subst /input_data/taxonomy.json,,$<) && \
	bash ./run.sh make load_data