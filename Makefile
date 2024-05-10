AGENT_TAG ?= sema-agent

BACKEND_CORE_PATH ?= ../backend-core
BACKEND_ACTIVITYPERSISTENCE_PATH ?= ../backend-activitypersistence
BACKEND_COMMITANALYSIS_PATH ?= ../backend-commitanalysis
BACKEND_GITBLAME_PATH ?= ../backend-gitblame
AI_ENGINE_PATH ?= ../ai_engine

.PHONY: all build-jars ai-engine-models build run-docker run shell clean lint

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

out/ai_engine.tar.gz: $(AI_ENGINE_PATH)
	tar -czf out/ai_engine.tar.gz --exclude='.git*' --exclude='.github' --exclude='.vscode' --exclude='.husky' -C $(AI_ENGINE_PATH) .

ai-engine-models: $(AI_ENGINE_PATH)/.env.production
	$(eval include $(AI_ENGINE_PATH)/.env.production)
	aws s3 sync "s3://sagemaker-ai-code-monitor-experiments/${TUNED_MODEL}" "out/${TUNED_MODEL}"

$(eval $(call build-jar,$(BACKEND_CORE_PATH),))
$(eval $(call build-jar,$(BACKEND_ACTIVITYPERSISTENCE_PATH),out/backend-core/backend-core.jar))
$(eval $(call build-jar,$(BACKEND_COMMITANALYSIS_PATH),out/backend-activitypersistence/backend-activitypersistence.jar))
$(eval $(call build-jar,$(BACKEND_GITBLAME_PATH),out/backend-core/backend-core.jar))
build-jars: out/backend-commitanalysis/backend-commitanalysis.jar out/backend-gitblame/backend-gitblame.jar

build: build-jars out/ai_engine.tar.gz ai-engine-models
	# Build and tag the build stages separately, to prevent cleanup with `docker system prune`
	docker build --platform linux/amd64 --tag $(AGENT_TAG)-build-cppcheck --file ./docker/Dockerfile --target build-cppcheck ./
	docker build --platform linux/amd64 --tag $(AGENT_TAG)-build-openssl --file ./docker/Dockerfile --target build-openssl ./
	docker build --platform linux/amd64 --tag $(AGENT_TAG) --file ./docker/Dockerfile ./

run-docker: build
	docker run \
		--mount type=bind,source="$(abspath $(AGENT_REPO))",target=/repo,readonly \
		--mount type=bind,source="$(abspath $(AGENT_OUT))",target=/out \
		--rm $(AGENT_RUN_ARGS) $(AGENT_TAG) $(AGENT_CLI_ARGS)

shell: AGENT_RUN_ARGS += --mount type=bind,source="$(abspath .)",target=/src -it --entrypoint /bin/bash
shell: AGENT_CLI_ARGS += -c "SHELL=/bin/bash poetry shell"
shell: run-docker

run: AGENT_CLI_ARGS += --repository /repo --output /out $(AGENT_ARGS)
run: run-docker

clean:
	rm -rf out

lint:
	docker run \
		--mount type=bind,source="$(abspath ./.hadolint.yaml)",target=/.config/hadolint.yaml \
		--rm --interactive hadolint/hadolint < docker/Dockerfile
