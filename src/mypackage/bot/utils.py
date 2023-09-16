from telebot.util import content_type_media, content_type_service

all_content_types = content_type_media + content_type_service


# Can be used to fill the required func parameter in the TeleBot.register_callback_query_handler method
def dummy_true(*args, **kwargs):
    return True
