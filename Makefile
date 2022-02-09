init:
	pip install -r requirements.txt

run:
	python -m dev_diary

test:
	pytest tests

proto:
	protoc --python_out=./dev_diary protos/*
