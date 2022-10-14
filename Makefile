PKG_VERSION=$$(more galaxy.yml|grep version|cut -d ' ' -f2)

.PHONY: build install

default: build install

build:
	@mkdir -p dist
	@ansible-galaxy collection build --output-path dist/ --force

install:
	@ansible-galaxy collection install dist/illumio-core-$(PKG_VERSION).tar.gz --upgrade --force
