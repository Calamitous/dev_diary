init:
	pip install -r requirements.txt

test:
	pytest tests

proto:
	protoc --python-out=./dev_diary protos/*
