import argparse


def define_arg_parser():
    parser = argparse.ArgumentParser(description='Launch the bot using polling.')
    parser.add_argument('config_path', metavar='Config path', type=str, help='path to the config file')
    parser.add_argument('-e', '--use-env-vars', action='store_true', help='override config with env vars')
    parser.add_argument(
        '-m',
        dest='config_env_mapping_path',
        metavar='<mapping path>',
        type=str,
        help='path to the config env mapping file'
    )
    return parser
