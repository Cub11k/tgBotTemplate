#!/bin/sh

if [ ! -f /config/config.toml ]; then
    cp /app/config.toml /config/
fi

if [ ! -f /config/config_env_mapping.toml ]; then
    cp /app/config_env_mapping.toml /config/
fi

echo "$@"
exec "$@"
