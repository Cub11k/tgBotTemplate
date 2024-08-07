# tgBotTemplate

Simple, but extensible template for telegram bot,
using [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
and [adaptix](https://github.com/reagento/dataclass-factory/tree/3.x/develop)

## Installation

```bash
git clone https://github.com/Cub11k/tgBotTemplate.git  # via HTTPS
# or
git clone git@github.com:Cub11k/tgBotTemplate.git  # via SSH

cd tgBotTemplate
```

- Change package name, description, version, author, homepage, etc. in `pyproject.toml`
- Create [virtual environment](https://docs.python.org/3/library/venv.html#creating-virtual-environments) or use the existing one
- [Activate](https://docs.python.org/3/library/venv.html#how-venvs-work) virtual environment
- Installation options
  - Install the package in editable mode
  - Install the dependencies from a lock-file without installing the package itself

```bash
# Option #1 - installing the package in editable mode
pip install -e .

# Option #2 - installing only the dependencies
pip install -r requirements.txt
```

## About requirements.txt

In this template, the `requirements.txt` file is in fact a lock-file, generated using `pip-compile`

It contains a fixed set dependencies with strictly fixed versions (`==`) and is crucial
for having stable reproducible builds in production. Not to be edited manually 
as it can lead to conflicts :heavy_exclamation_mark: :heavy_exclamation_mark:

If you want to change this file, e.g. your set of dependencies in `pyproject.toml` has changed,
or you want to update the versions of existing packages, simply run

```bash
# this will ensure that requirements.txt satisfies the constraints set in your project
# it will not change the versions of packages if they already satisfy the constraints set
pip-compile pyproject.toml -o requirements.txt

# to force the update use --upgrade or --upgrade-package for specific packages (can be used multiple times)
pip-compile pyproject.toml --upgrade -o requirements.txt
# or
pip-compile pyproject.toml --upgrade-package pytelegrambotapi --upgrade-package adaptix==3.0.0b7 -o requirements.txt
```

## Usage

Before running the bot you'll have to configure the environment
using the environment variables

| Environment variable    | Description                                                 | Allowed values                    |
|-------------------------|-------------------------------------------------------------|-----------------------------------|
| CONFIG_PATH             | Path to the config file to use                              | Default `config.toml`             |
| CONFIG_USE_ENV_VARS     | Override config file with environment variables             | `True`, `1`<br/>Default `False`   |
| CONFIG_ENV_MAPPING_PATH | Path to the file with mapping of config values and env vars | Default `config_env_mapping.toml` |

The simplest way to run the bot using long polling is to use the `launch-polling` script

```bash
launch-polling <path-to-the-config-file>
```

To get more details about the script, run it with the `--help` flag

```bash
launch-polling --help
```

To run the bot using webhook, you'll have to adjust the module `mybot:webhook`
according to the web-framework used

After that, you can launch the app using the web-server of your choice, e.g. `gunicorn`

```bash
gunicorn 'mybot:webhook_app()' --bind=$HOST:$PORT --workers-class=$WORKERS_CLASS
```

## Uninstall

```bash
pip uninstall <your-package-name>
```

Beware that `mybot` is not the package name, but the name of the module,
the package name is defined in `pyproject.toml`

## Manual usage with Docker

### Build image
In project root execute:

```bash
docker build -t tgbot .
```

### Run built image
In any case subsititute `token` with your Telegram Bot API Token

Run in interactive mode (TTY + stdin):

```bash
docker run -it --rm -e MYAPP_BOT_TOKEN=token tgbot
```

Run detached (in background) with restart policy:

```bash
docker run -d --restart unless-stopped -e MYAPP_BOT_TOKEN=token tgbot
```

Run detached with bind mounts:

```bash
docker run -d --restart unless-stopped -v ./config:/config -v ./logs:/logs -e MYAPP_BOT_TOKEN=token tgbot
```

## Usage with Docker Compose
By default provided `docker-compose.yml` will build project in new image and run it with redis instance as a state storage.

### Configuring your bot
Provide `.env` file with `MYAPP_BOT_TOKEN` set to your Telegram Bot API Token.

Also in `.env` you can pass any configuration in env vars form according to your `config.toml` and `config_env_mapping.toml`.

### Build & Run
```bash
docker compose up -d --build
```

### Stop
```bash
docker compose down
```

### Volumes
By default there are 4 volumes created by `docker-compose.yml`:

1. config - directory with `config.toml` and `config_env_mapping.toml` which are used by running instance
2. logs - directory with logs (by default loggers are write in stdout and in files in this directory)
3. redis-config - redis configuration
4. redis-data - redis data storage (for persistence)

## Contribution

Feel free to contribute to the project by creating issues and pull requests
