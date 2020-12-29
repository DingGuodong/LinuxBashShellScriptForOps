# Dockerfile tips

> [Dockerfile reference](https://docs.docker.com/engine/reference/builder/)

1. the shell script file should have executing bit

```shell
chmod +x docker-entrypoint.sh
```

2. the _[Base Image](https://docs.docker.com/glossary/#base_image)_  can use `alpine:latest` to decrease the size of
   docker image

3. use an absolute file path for ENTRYPOINT and CMD.
