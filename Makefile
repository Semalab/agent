AGENT_TAG ?= sema-agent

.PHONY: all build run-docker run shell save-cache

all: run

build:
	mkdir -p cache
	docker build --platform linux/amd64 --tag $(AGENT_TAG) --file ./docker/Dockerfile ./

run-docker: build save-cache
	docker run \
		--mount type=bind,source="$(abspath $(AGENT_REPO))",target=/repo,readonly \
		--mount type=bind,source="$(abspath $(AGENT_OUT))",target=/out \
		--rm $(AGENT_RUN_ARGS) $(AGENT_TAG) $(AGENT_CLI_ARGS)

shell: AGENT_RUN_ARGS += -it --entrypoint /bin/bash
shell: run-docker

run: AGENT_CLI_ARGS += --repository /repo --output /out
run: run-docker

save-cache:
	$(eval CONTAINER_ID=$(shell docker container create $(AGENT_TAG)))
	docker container cp $(CONTAINER_ID):dependencies/dependency-check/data/. ./cache/dependency-check
	docker container rm $(CONTAINER_ID)
