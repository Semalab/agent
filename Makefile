.PHONY: clean linux windows

clean:
	docker build -t agent-linux-runner -f ./docker/linux/Dockerfile.run ./
	docker run --mount type=bind,source=$$PWD,target=/repo agent-linux-runner rm -rf /repo/dist

dist: dist/
	mkdir dist

linux: dist
	docker build -t agent-linux-builder -f ./docker/linux/Dockerfile.build ./
	docker run --mount type=bind,source=$$PWD/dist,target=/dist agent-linux-builder \
		poetry run pyinstaller --onefile --clean --noconfirm --dist /dist/linux --workpath /tmp /src/main.py

windows: dist
	docker build -t agent-windows-base -f ./docker/windows/Dockerfile.base ./
	docker build -t agent-windows-builder -f ./docker/windows/Dockerfile.build ./
	docker run --mount type=bind,source=$$PWD/dist,target=/dist agent-windows-builder \
		/scripts/wine-do.sh poetry run pyinstaller --onefile --clean --noconfirm --dist /dist/windows --workpath /tmp /src/main.py
