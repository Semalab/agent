AGENT_TAG ?= sema-agent

BACKEND_CORE_PATH ?= ../backend-core
BACKEND_ACTIVITYPERSISTENCE_PATH ?= ../backend-activitypersistence
BACKEND_COMMITANALYSIS_PATH ?= ../backend-commitanalysis
BACKEND_GITBLAME_PATH ?= ../backend-gitblame
AI_ENGINE_PATH ?= ../ai_engine

.PHONY: all build-jars build run-docker run shell clean lint

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

add_ai_engine:
	mkdir -p out/ai_engine \;
	rsync -a  --exclude='.git*' --exclude='.github' --exclude='.vscode' --exclude='.husky' ../ai_engine/ out/ai_engine/
	mv out/ai_engine/.env.production out/ai_engine/.env

$(eval $(call build-jar,$(BACKEND_CORE_PATH),))
$(eval $(call build-jar,$(BACKEND_ACTIVITYPERSISTENCE_PATH),out/backend-core/backend-core.jar))
$(eval $(call build-jar,$(BACKEND_COMMITANALYSIS_PATH),out/backend-activitypersistence/backend-activitypersistence.jar))
$(eval $(call build-jar,$(BACKEND_GITBLAME_PATH),out/backend-core/backend-core.jar))
build-jars: add_ai_engine out/backend-commitanalysis/backend-commitanalysis.jar out/backend-gitblame/backend-gitblame.jar 

build: build-jars
	docker build --platform linux/amd64 --tag $(AGENT_TAG) --file ./docker/Dockerfile ./

run-docker: build
	docker run \
		--mount type=bind,source="$(abspath $(AGENT_REPO))",target=/repo,readonly \
		--mount type=bind,source="$(abspath $(AGENT_OUT))",target=/out \
		--rm $(AGENT_RUN_ARGS) $(AGENT_TAG) $(AGENT_CLI_ARGS)

shell: AGENT_RUN_ARGS += -it --entrypoint /bin/bash
shell: run-docker

run: AGENT_CLI_ARGS += --repository /repo --output /out $(AGENT_ARGS)
run: run-docker

clean:
	rm -rf out

lint:
	docker run \
		--mount type=bind,source="$(abspath ./.hadolint.yaml)",target=/.config/hadolint.yaml \
		--rm --interactive hadolint/hadolint < docker/Dockerfile
