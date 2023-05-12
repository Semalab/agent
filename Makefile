build:
	docker build -t agent-py-builder ./docker-build/
	docker run --mount type=bind,source=$$PWD,target=/code agent-py-builder windows
