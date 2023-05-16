linux:
	docker build -t agent-linux-builder -f ./docker/linux/Dockerfile.build ./
	docker run --mount type=bind,source=$$PWD/dist,target=/dist agent-linux-builder \
		poetry run pyinstaller --onefile --clean --noconfirm --dist /dist/linux --workpath /tmp /src/main.py

windows:
	docker build -t agent-py-windows-builder -f ./docker/windows/Dockerfile.build ./
	docker run --mount type=bind,source=$$PWD,target=/code agent-py-windows-builder \
		/scripts/wine-do.sh pyinstaller --onefile --clean --noconfirm --dist /code/dist/windows --workpath /tmp /code/agent/main.py
