init:
	pip install -r requirements.txt

run:
	python -m dev_diary

run-testfile:
	python -m dev_diary dev_diary.json

build:
	make init
	make proto
	make format

test:
	pytest tests

format:
	black .

proto:
	protoc --python_out=./dev_diary protos/*

logwatch:
	rm out.log && touch out.log && reset && tail -f out.log
