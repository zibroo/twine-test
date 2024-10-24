.PHONY: build package publish all

TARGET := $(target)
REPO_NAME := $(shell basename `git rev-parse --show-toplevel`)
VERSION := $(shell git rev-parse --short HEAD)
BUILD_NUMBER := $(build_number)
PACKAGE := $(TARGET)-$(BUILD_NUMBER).tar.gz
ARTIFACTORY_URL := $(url)


package:
	# Build the Python package using setup.py
	pip install --upgrade pip ;\
	pip install --upgrade setuptools ;\
	pip install wheel twine ;\
	cd src/$(TARGET) ;\
	python setup.py sdist bdist_wheel ;\
    # twine check *

publish:
	export ARTIFACTORY_PACKAGE=pypi-local/adelphic/$(REPO_NAME)/$(TARGET) ;\
	export ARTIFACTORY_URL=$(ARTIFACTORY_URL) ; \
	export ARTIFACTORY_SOURCE=$(PACKAGE) ; \
	export BUILD_NUMBER=$(BUILD_NUMBER) ;\
	twine upload --repository-url$(ARTIFACTORY_URL) src/$(TARGET)/dist/* ;\
	

all: package