from aiogram.fsm.state import State, StatesGroup

class Adverts(StatesGroup):
    adverts = State()

class ChannelState(StatesGroup):
    kanal_qoshish = State()


class DelChannelState(StatesGroup):
    delete_channel = State()