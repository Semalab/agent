linux:
	docker build -t agent-py-linux-builder -f ./docker-build/Dockerfile.linux ./docker-build
	docker run --mount type=bind,source=$$PWD,target=/code agent-py-linux-builder

windows:
	docker build -t agent-py-windows-builder -f ./docker-build/Dockerfile.windows ./docker-build
	docker run --mount type=bind,source=$$PWD,target=/code agent-py-windows-builder
