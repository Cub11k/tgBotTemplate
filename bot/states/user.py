from telebot.handler_backends import State, StatesGroup


class UserStates(StatesGroup):
    state_1 = State()
    state_2 = State()
