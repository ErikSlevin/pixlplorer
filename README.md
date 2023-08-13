# pixlplorer

docker-cli

```shell
docker run -d --name pixlplorer --hostname pixplorer \
    -p 5000:5000 \
    -e DB_HOST=localhost \
    -e DB_NAME=pixlplorer \
    -e DB_USER=root \
    -e DB_PASSWORD==myPassword \
    -e SECRET_KEY=RAnd0mChaRs \
    pixlplorer
```

docker-compose.yml
```yaml
version: '3'

services:
  pixlplorer:

    image: pixlplorer
    container_name: pixlplorer
    hostname: pixplorer

    ports:
      - "5000:5000"

    environment:
      - DB_HOST=localhost
      - DB_NAME=pixlplorer
      - DB_USER=root
      - DB_PASSWORD=myPassword
      - SECRET_KEY=RAnd0mChaRs

    volumes:
      - type: bind
        source:  /home/erik/configs/docker/pixlplorer/config.py
        target: /app/config.py
      - pixlplorer-upload:/app/uploads

volumes:
  pixlplorer-upload:

```

