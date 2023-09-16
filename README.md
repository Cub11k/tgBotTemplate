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
- Create [virtual environment](https://docs.python.org/3/library/venv.html#creating-virtual-environments) or use the
  existing one
- [Activate](https://docs.python.org/3/library/venv.html#how-venvs-work) virtual environment
- Install the package in editable mode

```bash
pip install -e .
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

To run the bot using webhook, you'll have to adjust the module `mypackage:webhook`
according to the web-framework used

After that, you can launch the app using the web-server of your choice, e.g. `gunicorn`

```bash
gunicorn 'mypackage:webhook_app()' --bind=$HOST:$PORT --workers-class=$WORKERS_CLASS
```

## Uninstall

```bash
pip uninstall <your-package-name>
```

Beware that `mypackage` is not the package name, but the name of the module,
the package name is defined in `pyproject.toml`

## Contribution

Feel free to contribute to the project by creating issues and pull requests
