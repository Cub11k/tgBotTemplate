from telebot.types import Update


def tg_update_handler(request):
    secret_token = request.app.ctx.secret_token  # TODO: get secret token from somewhere, e.g. from the app context
    if secret_token != request.headers.get('X-Telegram-Bot-Api-Secret-Token'):
        request.app.ctx.logger.debug(f"Invalid secret-token request from {request.remote}")  # TODO: Adjust if necessary
        return 'Forbidden', 403
    body_json = request.json()
    bot = request.app.ctx.bot  # TODO: get bot from somewhere, e.g. from the app context
    update = Update.de_json(body_json)
    bot.process_new_updates([update])
    request.app.ctx.logger.debug(f"Processed update {update.update_id}")  # TODO: Adjust if necessary
    return 'OK', 200
