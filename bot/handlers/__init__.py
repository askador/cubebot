from aiogram import Dispatcher

from . import errors
from . import users
from . import groups
from . import default_commands


def setup(dp: Dispatcher):
    default_commands.register_default_handlers(dp)
    users.register_users_handlers(dp)
    groups.register_groups_handlers(dp)
    errors.register_errors_handlers(dp)
    