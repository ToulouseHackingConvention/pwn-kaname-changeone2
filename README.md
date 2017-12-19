# Changebyone

- Author : Kaname
- Type : special pwn
- Docker image : pwn-kaname-changebyone2

## Description

Goal : get a shell

nc localhost 5797

## Files provided to the challengers

- changebyone2
- changebyone2.c
- changebyone.py
- libc.so.6

## Build the docker image

`make build`

## Run the docker container

`make up`

## Export the files

`make export`

## Update the flag

Update `flag` before running `make up`
