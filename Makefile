AGENT_TAG ?= sema-agent

BACKEND_CORE_PATH ?= ../backend-core
BACKEND_ACTIVITYPERSISTENCE_PATH ?= ../backend-activitypersistence
BACKEND_COMMITANALYSIS_PATH ?= ../backend-commitanalysis
BACKEND_GITBLAME_PATH ?= ../backend-gitblame

.PHONY: all build-jars build run-docker run shell save-cache clean

all: run

define build-jar
out/$(notdir $(1))/$(notdir $(1)).jar: $(1)/pom.xml $(1)/src $(2)
	docker run \
		-v maven-repo:/root/.m2 \
		-v "$(abspath $(1)):/usr/src/mymaven" \
		-w /usr/src/mymaven \
		--rm maven mvn clean install
	mkdir -p out/$(notdir $(1))
	cp $(1)/target/*.jar out/$(notdir $(1))
endef

$(eval $(call build-jar,$(BACKEND_CORE_PATH),))
$(eval $(call build-jar,$(BACKEND_ACTIVITYPERSISTENCE_PATH),out/backend-core/backend-core.jar))
$(eval $(call build-jar,$(BACKEND_COMMITANALYSIS_PATH),out/backend-activitypersistence/backend-activitypersistence.jar))
$(eval $(call build-jar,$(BACKEND_GITBLAME_PATH),out/backend-gitblame/backend-gitblame.jar))

build-jars: out/backend-commitanalysis/backend-commitanalysis.jar out/backend-gitblame/backend-gitblame.jar

build: build-jars
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

clean:
	rm -rf out
