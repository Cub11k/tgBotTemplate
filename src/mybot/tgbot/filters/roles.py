from telebot.custom_filters import SimpleCustomFilter


class IsOwnerFilter(SimpleCustomFilter):
    key = 'is_owner'

    def __init__(self, owner_tg_id: int):
        super().__init__()
        self.owner_tg_id = owner_tg_id

    # argument naming is kept from the base class to avoid possible errors if passed as kwargs
    # message is an update
    def check(self, message):
        return message.from_user.id == self.owner_tg_id
