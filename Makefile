SHELL := /bin/bash
DOCKER ?= docker
GRADLEW ?= ./gradlew
IMAGE_NAME := 'phoenix-service-categories-classification'
CONTAINER_NAME := 'phoenix-nn'
USERNAME := 'bsgfb'

DOCKER_BUILD := ${DOCKER} build -t ${IMAGE_NAME} .
DOCKER_RUN := ${DOCKER} run -it --rm --name ${CONTAINER_NAME} -p 5001:5001 -e MODEL_NAME=26_5_2018__15_24 -d ${IMAGE_NAME}

build:
	${DOCKER_BUILD}

run:
	${DOCKER_RUN}

full:
	${DOCKER_BUILD}
	${DOCKER_RUN}

stop:
	${DOCKER} stop ${CONTAINER_NAME}

push:
	${DOCKER_BUILD}
	${DOCKER} tag ${IMAGE_NAME} ${USERNAME}/${IMAGE_NAME}
	${DOCKER} push ${USERNAME}/${IMAGE_NAME}
