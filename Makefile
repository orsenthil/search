.DEFAULT_GOAL := help

DOCKER_IMAGE_NAME = search

.PHONY: build
build: ## build the docker image for platform linux/amd64 using docker buildx build
build:
	docker buildx build --platform linux/amd64 -t $(DOCKER_IMAGE_NAME) .

.PHONY: tag
tag: ## tag the docker image as skumaran/search:latest
tag:
	docker tag $(DOCKER_IMAGE_NAME):latest skumaran/$(DOCKER_IMAGE_NAME):latest

.PHONY: push
push: ## push the docker image to docker hub
push:
	docker push skumaran/$(DOCKER_IMAGE_NAME):latest

login:
	docker login

all: login build tag push ## Build, tag and push the docker image

.PHONY: install-minikube
install-minikube: ## Install minikube
install-minikube:
	brew install minikube

.PHONY: start-minikube
start-minikube: ## Start default Kubernetes Cluster in minikube
start-minikube:
	minikube start

.PHONY: deploy-app-in-minikube
deploy-app-in-minikube: ## Deploy the search app in minikube
deploy-app-in-minikube:
	kubectl apply -f k8s/app.yaml

.PHONY: launch-app
launch-app: ## Launch the search app
launch-app: deploy-app-in-minikube
	minikube service search

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

define print-target
    @printf "Executing target: \033[36m$@\033[0m\n"
endef
