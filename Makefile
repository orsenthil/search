# target build to build the docker image

DOCKER_IMAGE_NAME = search

build:
	docker buildx build --platform linux/amd64 -t $(DOCKER_IMAGE_NAME) .

tag:
	docker tag $(DOCKER_IMAGE_NAME):latest skumaran/$(DOCKER_IMAGE_NAME):latest

push:
	docker push skumaran/$(DOCKER_IMAGE_NAME):latest

login:
	docker login

all: login build tag push

install-minikube:
	brew install minikube

start-minikube:
	minikube start
