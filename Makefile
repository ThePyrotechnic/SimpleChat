.PHONY: init web app clean

SIMPLECHAT_ENV_FILE ?= .env.local

init:
	@cd app && $(MAKE) init
	cd web && $(MAKE) init

web:
	cd web && $(MAKE) run

app:
	cd app && $(MAKE) run SIMPLECHAT_ENV_FILE=$(SIMPLECHAT_ENV_FILE)

clean:
	cd app && $(MAKE) clean
	cd web && $(MAKE) clean