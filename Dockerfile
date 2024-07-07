FROM python:3.10-slim

## prepare environment
RUN pip install pip-tools

RUN mkdir /app /config /logs
RUN useradd -ms /bin/sh bot

WORKDIR /app
##

## use pip-compile to install only requirements
COPY pyproject.toml /app/

RUN pip-compile -o requirements.txt pyproject.toml
RUN pip install -r requirements.txt
##

## copy entrypoint
COPY docker-entrypoint.sh /
##

## copy sources and install package
COPY src /app/src/
COPY config.toml config_env_mapping.toml /app/

RUN pip install .
##

## set some defaults
ENV STATE_STORAGE_TYPE=memory
##

## set user and workdir
RUN chown -R bot:bot /app /config /logs
RUN chmod +x /docker-entrypoint.sh

USER bot

WORKDIR /
##

## define entrypoint and cmd
ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["launch-polling", "-e", "-m", "/config/config_env_mapping.toml", "/config/config.toml"]
##

## define volumes
VOLUME /config
VOLUME /logs
##
