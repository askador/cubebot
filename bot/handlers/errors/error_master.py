from loguru import logger
from time import sleep
from aiogram.types import Update
from aiogram.utils.exceptions import (
    Unauthorized, Throttled, ChatNotFound, 
    StartParamInvalid, TelegramAPIError,
    MessageNotModified, MessageToDeleteNotFound,
    MessageCantBeEdited, MessageToEditNotFound,
    MessageTextIsEmpty, RetryAfter,
    CantParseEntities, MessageCantBeDeleted, 
    ValidationError, FSMStorageWarning, 
    TimeoutWarning, AIOGramWarning, 
    BotKicked, BotBlocked, 
    UserDeactivated, NetworkError,
    MessageIdInvalid, MessageToReplyNotFound
)


async def errors_handler(update: Update, exception, *args, **kwargs):
    """
    Exceptions handler. Catches all exceptions within task factory tasks.
    :param update:
    :param exception:
    :return: stdout logger
    """

    if isinstance(exception, ValidationError):
        logger.exception(f'ValidationError: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, Throttled):
        logger.error(f"Throttled: {exception} \nUpdate: {update}")
        return True

    if isinstance(exception, ChatNotFound):
        logger.exception(f"ChatNotFound: {exception} \nUpdate: {update}")
        return True

    if isinstance(exception, UserDeactivated):
        logger.error(f"UserDeactivated: {exception} \nUpdate: {update}")
        return True

    if isinstance(exception, StartParamInvalid):
        logger.error(f"StartParamInvalid: {exception} \nUpdate: {update}")
        return True

    if isinstance(exception, NetworkError):
        logger.exception(f"NetworkError: {exception} \nUpdate: {update}")
        return True

    if isinstance(exception, MessageNotModified):
        logger.error('Message is not modified')
        return True

    if isinstance(exception, MessageIdInvalid):
        logger.error('MessageId is invalid')
        return True

    if isinstance(exception, MessageCantBeDeleted):
        logger.error('Message cant be deleted')
        return True

    if isinstance(exception, MessageToDeleteNotFound):
        logger.error('Message to delete not found')
        return True

    if isinstance(exception, MessageCantBeEdited):
        logger.error('Message cant be edited')
        return True

    if isinstance(exception, MessageToEditNotFound):
        logger.error('Message to edit not found')
        return True

    if isinstance(exception, MessageToReplyNotFound):
        logger.error('Message to reply not found')
        return True

    if isinstance(exception, MessageTextIsEmpty):
        logger.error('MessageTextIsEmpty')
        return True

    if isinstance(exception, Unauthorized):
        logger.exception(f'Unauthorized: {exception}')
        return True

    if isinstance(exception, TelegramAPIError):
        logger.error(f'TelegramAPIError: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, RetryAfter):
        logger.error(f'RetryAfter: {exception} \nUpdate: {update}')
        sleep(exception.timeout)
        return True

    if isinstance(exception, CantParseEntities):
        logger.error(f'CantParseEntities: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, FSMStorageWarning):
        logger.warning(f'FSMStorageWarning: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, TimeoutWarning):
        logger.warning(f'TimeoutWarning: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, AIOGramWarning):
        logger.warning(f'AIOGramWarning: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, BotKicked):
        logger.error(f'BotKicked: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, BotBlocked):
        logger.error(f'BotBlocked: {exception} \nUpdate: {update}')
        return True

    logger.exception(f'Update: {update} \n{exception}')
    return True
