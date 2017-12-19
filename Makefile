IMG = pwn-kaname-changebyone2
CTN = changebyone2

build:
	docker build -t $(IMG) .

export: build
	mkdir -p export
	docker run --rm --entrypoint cat $(IMG) /srv/changebyone2 > export/changebyone2
	docker run --rm --entrypoint cat $(IMG) /lib/x86_64-linux-gnu/libc.so.6 > export/libc.so.6
	cp src/changebyone2.c src/changebyone.py export/

up: build
	docker run -d -p 5797:5797 --name $(CTN) $(IMG)

down:
	-docker rm -f $(CTN)

logs:
	docker logs -f $(CTN)

clean: down
	-docker rmi $(IMG)
	rm -rf export

.PHONY: build export up down logs clean
