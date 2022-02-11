import logging
import time

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

HANDLED_STR = ['Unhandled', 'Handled']


class LoggingMiddleware(BaseMiddleware):
    def __init__(self, logger=__name__):
        if not isinstance(logger, logging.Logger):
            logger = logging.getLogger(logger)

        self.logger = logger

        super(LoggingMiddleware, self).__init__()

    def check_timeout(self, obj):
        start = obj.conf.get('_start', None)
        if start:
            del obj.conf['_start']
            return round((time.time() - start) * 1000)
        return -1

    async def on_pre_process_update(self, update: types.Update, data: dict):
        update.conf['_start'] = time.time()
        self.logger.debug(f"Received update [ID:{update.update_id}]")

    async def on_post_process_update(self, update: types.Update, result, data: dict):
        timeout = self.check_timeout(update)
        if timeout > 0:
            self.logger.info(f"Process update [ID:{update.update_id}]: [success] (in {timeout} ms)")

    async def on_pre_process_message(self, message: types.Message, data: dict):
        self.logger.info(f"Received message [ID:{message.message_id}] in chat [{message.chat.type}:{message.chat.id}]")

    async def on_post_process_message(self, message: types.Message, results, data: dict):
        self.logger.debug(f"{HANDLED_STR[bool(len(results))]} "
                          f"message [ID:{message.message_id}] in chat [{message.chat.type}:{message.chat.id}]")

    async def on_pre_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        if callback_query.message:
            message = callback_query.message
            text = (f"Received callback query [ID:{callback_query.id}] "
                    f"from user [ID:{callback_query.from_user.id}] "
                    f"for message [ID:{message.message_id}] "
                    f"in chat [{message.chat.type}:{message.chat.id}] "
                    f"with data: {callback_query.data}")

            if message.from_user:
                text = f"{text} originally posted by user [ID:{message.from_user.id}]"

            self.logger.info(text)

        else:
            self.logger.info(f"Received callback query [ID:{callback_query.id}] "
                             f"from user [ID:{callback_query.from_user.id}] "
                             f"for inline message [ID:{callback_query.inline_message_id}] ")

    async def on_post_process_callback_query(self, callback_query, results, data: dict):
        if callback_query.message:
            message = callback_query.message
            text = (f"{HANDLED_STR[bool(len(results))]} "
                    f"callback query [ID:{callback_query.id}] "
                    f"from user [ID:{callback_query.from_user.id}] "
                    f"for message [ID:{message.message_id}] "
                    f"in chat [{message.chat.type}:{message.chat.id}] "
                    f"with data: {callback_query.data}")

            if message.from_user:
                text = f"{text} originally posted by user [ID:{message.from_user.id}]"

            self.logger.info(text)

        else:
            self.logger.debug(f"{HANDLED_STR[bool(len(results))]} "
                              f"callback query [ID:{callback_query.id}] "
                              f"from user [ID:{callback_query.from_user.id}]"
                              f"from inline message [ID:{callback_query.inline_message_id}]")

    async def on_pre_process_error(self, update, error, data: dict):
        timeout = self.check_timeout(update)
        if timeout > 0:
            self.logger.info(f"Process update [ID:{update.update_id}]: [failed] (in {timeout} ms)")


    async def on_post_process_my_chat_member(self, my_chat_member_update, results, data):
        self.logger.debug(f"{HANDLED_STR[bool(len(results))]} my_chat_member "
                          f"for user [ID:{my_chat_member_update.from_user.id}]")

    async def on_pre_process_chat_member(self, chat_member_update, data):
        self.logger.info(f"Received chat member update "
                         f"for user [ID:{chat_member_update.from_user.id}]. "
                         f"Old state: {chat_member_update.old_chat_member.to_python()} "
                         f"New state: {chat_member_update.new_chat_member.to_python()} ")

    async def on_post_process_chat_member(self, chat_member_update, results, data):
        self.logger.debug(f"{HANDLED_STR[bool(len(results))]} chat_member "
                          f"for user [ID:{chat_member_update.from_user.id}]")
