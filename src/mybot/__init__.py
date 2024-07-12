import os

from .tgbot import setup_bot, launch_bot
from .cli import define_arg_parser
from .config import load_config
from .logger import setup_logger
from .webhook import setup_app, Application


def webhook_app() -> Application:
    # this function is just an example of how you can create the app factory
    config_path = os.environ.get('CONFIG_PATH', 'config.toml')
    use_env_vars = os.environ.get('CONFIG_USE_ENV_VARS', False) in ('1', 'true', 'True', 'TRUE')
    config_env_mapping_path = os.environ.get('CONFIG_ENV_MAPPING_PATH', 'config_env_mapping.toml')
    cfg = load_config(config_path, use_env_vars, config_env_mapping_path)
    app_logger = setup_logger(cfg.logger)
    app_logger.debug(f"Config loaded: {cfg=}")
    app_logger.debug(f"Setting up the bot logger: {cfg.bot.logger=}")

    bot_logger = setup_logger(cfg.bot.logger)
    app_logger.debug(f"Setting up the bot: {cfg.bot=}, {cfg.messages=}, {cfg.buttons=}")
    bot_ = setup_bot(cfg.bot, cfg.messages, cfg.buttons, bot_logger)

    app_logger.debug(f"Setting up the web-app: {cfg.bot.webhook.path=}")
    app = setup_app(cfg.bot.webhook.path)
    app.ctx.bot = bot_
    app.ctx.secret_token = cfg.bot.webhook.secret_token
    app.ctx.logger = app_logger

    app_logger.info("Launching the bot")
    app_logger.debug(
        f"Launching the bot with webhook: {cfg.bot.drop_pending=}, {cfg.bot.allowed_updates=}, {cfg.bot.webhook=}"
    )
    # use_webhook is intentionally hard-coded to True here as we're using webhook
    launch_bot(bot_, cfg.bot.drop_pending, True, cfg.bot.allowed_updates, cfg.bot.webhook)
    return app


def main():
    # If you wish to use webhook, you'll probably want to launch the bot using the web-server, e.g. gunicorn
    # In this case you should be calling the webhook_app_factory function
    arg_parser = define_arg_parser()
    args = arg_parser.parse_args()
    config_path = os.environ.get('CONFIG_PATH', args.config_path)
    use_env_vars = os.environ.get('CONFIG_USE_ENV_VARS', args.use_env_vars) in ('1', 'true', 'True', 'TRUE', True)
    config_env_mapping_path = os.environ.get('CONFIG_ENV_MAPPING_PATH', args.config_env_mapping_path)
    cfg = load_config(config_path, use_env_vars, config_env_mapping_path)
    app_logger = setup_logger(cfg.logger)
    app_logger.debug(f"Config loaded: {cfg=}")
    app_logger.debug(f"Setting up the bot logger: {cfg.bot.logger=}")
    bot_logger = setup_logger(cfg.bot.logger)
    app_logger.debug(f"Setting up the bot: {cfg.bot=}, {cfg.messages=}, {cfg.buttons=}")
    bot_ = setup_bot(cfg.bot, cfg.messages, cfg.buttons, bot_logger)
    app_logger.info("Launching the bot")
    app_logger.debug(f"Launching the bot with polling: {cfg.bot.drop_pending=}, {cfg.bot.allowed_updates=}")
    # use_webhook is intentionally hard-coded to False here as we're using long polling
    launch_bot(bot_, cfg.bot.drop_pending, False, cfg.bot.allowed_updates)
