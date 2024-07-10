import collections
import os
import sys
from typing import Optional

from adaptix import Retort

if sys.version_info >= (3, 11):
    import tomllib
    from tomllib import TOMLDecodeError
else:
    from toml import TomlDecodeError as TOMLDecodeError
    import toml as tomllib

from .models import Config


def is_dict_subset(sub: dict, full: dict) -> bool:
    """
    Check if 'sub' is a subset of 'full' dictionary.

    Args:
        sub (dict): The dictionary to check if it is a subset.
        full (dict): The dictionary to check against.

    Returns:
        bool: True if 'sub' is a subset of 'full', False otherwise.
    """
    queue = collections.deque([(sub, full)])
    while queue:
        cur1, cur2 = queue.popleft()

        if not cur1.keys() <= cur2.keys():
            return False

        for key in cur1:
            is_dict_cur1 = isinstance(cur1[key], dict)
            is_dict_cur2 = isinstance(cur2[key], dict)
            if is_dict_cur1 and is_dict_cur2:
                queue.append((cur1[key], cur2[key]))
            elif is_dict_cur1 or is_dict_cur2:
                return False
    return True


def calculate_config_env_mapping(config_data: dict) -> dict:
    """
    Calculate the config env mapping.

    Args:
        config_data (dict): The configuration data.

    Returns:
        dict: The mapping of config keys to environment variable names.
    """
    mapping = {}
    queue = collections.deque([(config_data, mapping, None)])
    while queue:
        current_data, current_mapping, prefix = queue.popleft()
        for key, value in current_data.items():
            key_name = f'{prefix}_{key.upper()}' if prefix else key.upper()
            if isinstance(value, dict):
                current_mapping[key] = {}
                queue.append((value, current_mapping[key], key_name))
            else:
                current_mapping[key] = key_name
    return mapping


def override_config_with_env_vars(config_data: dict, config_env_mapping: dict, env_vars: dict) -> dict:
    """
    Override the config data with environment variables based on the config env mapping.

    Args:
        config_data (dict): The original config data.
        config_env_mapping (dict): The mapping between config keys and environment variable names.
        env_vars (dict): A dictionary of environment variables.

    Returns:
        dict: The updated config data with environment variable values.

    Raises:
        ValueError: If the config and config env mapping keys are not compatible.
    """
    if not is_dict_subset(config_data, config_env_mapping):
        raise ValueError('Config and config env mapping keys are not compatible')

    config_data_copy = config_data.copy()
    queue = collections.deque([(config_data_copy, config_env_mapping)])
    while queue:
        current1, current2 = queue.popleft()
        for key in current1.keys():
            if isinstance(current1[key], dict):
                queue.append((current1[key], current2[key]))
            else:
                env_var = current2[key]
                if env_var and env_var in env_vars:
                    current1[key] = env_vars[env_var]
    return config_data_copy


def parse_config_file(config_path: str) -> dict:
    """
    Parse the config file and return a dictionary.

    Args:
        config_path: The path to the config file.

    Returns:
        A dictionary containing the parsed config.

    Raises:
        FileNotFoundError: If the config file does not exist or is not accessible.
        ValueError: If there is an error parsing the config file.
    """
    if not os.path.isfile(config_path):
        raise FileNotFoundError(f"File '{config_path}' does not exist or is not accessible.")

    try:
        with open(config_path, 'r') as f:
            return tomllib.loads(f.read())
    except TOMLDecodeError as e:
        raise ValueError(f"Error parsing config file: {e}")


def parse_config_env_mapping_file(config_env_mapping_path: str) -> dict:
    """
    Parse the configuration environment mapping file and return a dictionary.

    Args:
        config_env_mapping_path: The path to the configuration environment mapping file.

    Returns:
        A dictionary containing the parsed configuration environment mapping.

    Raises:
        FileNotFoundError: If the configuration environment mapping file is not found.
        ValueError: If there is an error parsing the configuration environment mapping file.
    """
    try:
        return parse_config_file(config_env_mapping_path)
    except FileNotFoundError as e:
        raise e
    except ValueError as e:
        raise ValueError(f"Error parsing config env mapping file: {e}")


def create_retort(strict_coercion: bool, *args, **kwargs) -> Retort:
    """
    Create a Retort instance with the given strict_coercion and additional arguments.

    Parameters:
        strict_coercion (bool): Whether to use strict coercion.
        *args: Additional arguments to pass to the Retort instance.
        **kwargs: Additional keyword arguments to pass to the Retort instance.

    Returns:
        Retort: The created Retort instance.
    """
    # TODO: this function should probably be moved to the separate file / module, but for the sake of simplicity
    # of the template I'm keeping it here

    # TODO: add any extra arguments, schemas, validators, etc. to the Retort instance if you have to
    return Retort(strict_coercion=strict_coercion, *args, **kwargs)


def load_config(config_path: str,
                use_env_vars: bool,
                config_env_mapping_path: Optional[str] = None,
                env_vars: Optional[dict[str, str]] = None) -> Config:
    """
    Load the configuration from a file and optionally override it with environment variables.

    Args:
        config_path: The path to the configuration file.
        use_env_vars: A flag indicating whether to override the configuration with environment variables.
        config_env_mapping_path: The path to the configuration environment mapping file.
        env_vars: A dictionary of environment variables.

    Returns:
        The loaded configuration.
    """
    config_data = parse_config_file(config_path)  # load the initial config from file
    if use_env_vars:
        if config_env_mapping_path is not None:
            config_env_mapping = parse_config_env_mapping_file(config_env_mapping_path)
        else:
            config_env_mapping = calculate_config_env_mapping(config_data)

        if env_vars is None:
            env_vars = os.environ

        config_data = override_config_with_env_vars(config_data, config_env_mapping, env_vars)

    retort = create_retort(strict_coercion=False)
    return retort.load(config_data, Config)  # load the Config model, all data validation will happen there
