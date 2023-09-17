import os
from typing import Optional

from adaptix import Retort

try:
    import tomllib
except ImportError:
    import toml as tomllib

from .models import Config


def is_subset_dict(sub: dict, full: dict) -> bool:
    # thus function uses a queue to iterate over the dicts instead of the recursive approach

    queue = [(sub, full)]
    while queue:
        cur1, cur2 = queue.pop(0)

        if not cur1.keys() <= cur2.keys():
            return False

        for key in cur1.keys():
            if all(isinstance(i[key], dict) for i in (cur1, cur2)):
                queue.append((cur1[key], cur2[key]))
            elif any(isinstance(i[key], dict) for i in (cur1, cur2)):
                return False
    return True


def calculate_config_env_mapping(config_data: dict) -> dict:
    # this function is just an example of how you can calculate the config env mapping
    # bot.token -> BOT_TOKEN; bot.state_storage.redis.host -> BOT_STATE_STORAGE_REDIS_HOST
    # it uses a queue to iterate over the config and create the mapping instead of the recursive approach

    mapping = {}
    queue = [(config_data, mapping, None)]
    while queue:
        current_data, current_mapping, prefix = queue.pop(0)
        for key in current_data.keys():
            key_name = f'{prefix}_{key.upper()}' if prefix else key.upper()
            if isinstance(current_data[key], dict):
                current_mapping[key] = {}
                queue.append((current_data[key], current_mapping[key], key_name))
            else:
                current_mapping[key] = key_name
    return mapping


def override_config_with_env_vars(config_data: dict, config_env_mapping: dict) -> dict:
    # this function might be a bit overcomplicated, but it's a good example of how you can override the config
    # without using the template renderer like jinja2
    # it uses a queue to iterate over the config and the mapping instead of the recursive approach

    queue = [(config_data, config_env_mapping)]
    while queue:
        current1, current2 = queue.pop(0)
        for key in current1.keys():
            if isinstance(current1[key], dict):
                queue.append((current1[key], current2[key]))
            else:
                env_var = current2[key]
                if env_var:
                    current1[key] = os.environ.get(env_var, current1[key])
    return config_data


def parse_config_file(config_path: str) -> dict:
    # this function is just a wrapper around the tomllib.load function
    # you can use any other config parser, e.g. pyyaml, toml, etc. and add any other parsing logic here

    with open(config_path, 'rb') as f:
        return tomllib.load(f)


def create_retort(strict_coercion: bool, *args, **kwargs) -> Retort:
    # TODO: this function should probably be moved to the separate file / module, but for the sake of simplicity
    # of the template I'm keeping it here

    # TODO: add any extra arguments, schemas, validators, etc. to the Retort instance if you have to
    return Retort(strict_coercion=strict_coercion, *args, **kwargs)


def load_config(config_path: str, use_env_vars: bool, config_env_mapping_path: Optional[str] = None) -> Config:
    config_data = parse_config_file(config_path)  # load the initial config from file
    if use_env_vars:
        if config_env_mapping_path is not None:
            config_env_mapping = parse_config_file(config_env_mapping_path)  # load the env mapping from file
        else:
            # you can define the mapping any other way, for example calculate it based on the keys from the config
            # e.g. bot.token -> BOT_TOKEN; bot.state_storage.redis.host -> BOT_STATE_STORAGE_REDIS_HOST
            config_env_mapping = calculate_config_env_mapping(config_data)

        # you can also use a template renderer like jinja2 to render the config from a template using env vars

        if not is_subset_dict(config_data, config_env_mapping):  # check if the config and the mapping are compatible
            raise ValueError('Config and config env mapping keys are not equal')
        config_data = override_config_with_env_vars(config_data, config_env_mapping)

    # non-strict coercion allows to use env vars without type casting, as all env vars are strings
    retort = create_retort(strict_coercion=False)
    return retort.load(config_data, Config)  # load the Config model, all data validation will happen there
