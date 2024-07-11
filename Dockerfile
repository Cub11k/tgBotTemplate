FROM python:3.10-slim

## prepare environment
RUN pip install pip-tools

RUN useradd -ms /bin/sh bot
RUN mkdir /config /logs
RUN chown -R bot:bot /config /logs

COPY --chmod=777 docker-entrypoint.sh /

WORKDIR /app
##

## install only requirements.txt
COPY pyproject.toml ./

RUN pip-compile -o requirements.txt pyproject.toml
RUN pip install -r requirements.txt
##

## install package
COPY src ./src/
COPY config.toml config_env_mapping.toml ./

RUN pip install .
##

ENV STATE_STORAGE_TYPE=memory
ENV MYAPP_LOGGER_FILE_PATH=/logs/myapp.log
ENV MYAPP_BOT_LOGGER_FILE_PATH=/logs/bot.log

USER bot
WORKDIR /

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["launch-polling", "-e", "-m", "/config/config_env_mapping.toml", "/config/config.toml"]

VOLUME /config
VOLUME /logs
