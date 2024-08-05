.PHONY: init run clean

init: .env.local app_rsa.pem keys/app_rsa_public.pem
	poetry install

build:
	mkdir build

keys:
	mkdir keys

app_rsa.pem app_rsa_public.pem: keys
	openssl genrsa -out keys/app_rsa.pem 4096
	openssl rsa -in keys/app_rsa.pem -out keys/app_rsa_public.pem -pubout -outform PEM

.env.local: build
	cp .env.example .env.local

run:
	SIMPLECHAT_ENV_FILE=$(SIMPLECHAT_ENV_FILE) poetry run simplechat

clean:
	-rm -r build
	-rm -r dist