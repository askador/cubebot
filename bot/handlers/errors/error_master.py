import asyncio
from loguru import logger
from aiogram.types import Update
from aiogram.utils.exceptions import (
    # Top level
        TelegramAPIError,
        AIOGramWarning,

        # TelegramAPIErrors
            ValidationError, Throttled, Unauthorized, 
            RetryAfter, NetworkError,

            # BadRequests

                # MessageError
                    MessageNotModified, MessageToDeleteNotFound,
                    MessageCantBeEdited, MessageToEditNotFound,
                    MessageTextIsEmpty, MessageCantBeDeleted, 
                    MessageIdInvalid, MessageToReplyNotFound,

                ChatNotFound, StartParamInvalid, CantParseEntities, 

            # Unauthorized
                BotKicked, BotBlocked, UserDeactivated, 

        # AIOGramWarnings
            FSMStorageWarning, TimeoutWarning
)


async def errors_handler(update: Update, exception, *args, **kwargs):
    """
    Exceptions handler. Catches all exceptions within task factory tasks.
    :param update:
    :param exception:
    :return: stdout logger
    """

    if isinstance(exception, MessageNotModified):
        logger.error(f'Message is not modified\nUpdate: {update}')
        return True

    if isinstance(exception, MessageIdInvalid):
        logger.error(f'MessageId is invalid\nUpdate: {update}')
        return True

    if isinstance(exception, MessageCantBeDeleted):
        logger.error(f'Message cant be deleted\nUpdate: {update}')
        return True

    if isinstance(exception, MessageToDeleteNotFound):
        logger.error(f'Message to delete not found\nUpdate: {update}')
        return True

    if isinstance(exception, MessageCantBeEdited):
        logger.error(f'Message cant be edited\nUpdate: {update}')
        return True

    if isinstance(exception, MessageToEditNotFound):
        logger.error(f'Message to edit not found\nUpdate: {update}')
        return True

    if isinstance(exception, MessageToReplyNotFound):
        logger.error(f'Message to reply not found\nUpdate: {update}')
        return True

    if isinstance(exception, MessageTextIsEmpty):
        logger.error(f'MessageTextIsEmpty\nUpdate: {update}')
        return True


    if isinstance(exception, TimeoutWarning):
        logger.warning(f'TimeoutWarning: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, FSMStorageWarning):
        logger.warning(f'FSMStorageWarning: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, AIOGramWarning):
        logger.warning(f'AIOGramWarning: {exception} \nUpdate: {update}')
        return True


    if isinstance(exception, CantParseEntities):
        logger.error(f'CantParseEntities: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, StartParamInvalid):
        logger.error(f"StartParamInvalid: {exception} \nUpdate: {update}")
        return True

    if isinstance(exception, ChatNotFound):
        logger.exception(f"ChatNotFound: {exception} \nUpdate: {update}")
        return True


    if isinstance(exception, BotKicked):
        logger.error(f'BotKicked: {exception}\nUpdate: {update}')
        return True

    if isinstance(exception, BotBlocked):
        logger.error(f'BotBlocked\nUpdate: {update}')
        return True
    
    if isinstance(exception, UserDeactivated):
        logger.error(f"UserDeactivated: {exception} \nUpdate: {update}")
        return True

    if isinstance(exception, Unauthorized):
        logger.exception(f'Unauthorized: {exception}')
        return True

        
    if isinstance(exception, Throttled):
        logger.error(f"Throttled: {exception} \nUpdate: {update}")
        return True

    if isinstance(exception, NetworkError):
        logger.exception(f"NetworkError: {exception} \nUpdate: {update}")
        return True
    
    if isinstance(exception, RetryAfter):
        logger.error(f'RetryAfter: {exception} \nUpdate: {update}')
        await asyncio.sleep(exception.timeout)
        return True

    if isinstance(exception, ValidationError):
        logger.exception(f'ValidationError: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, TelegramAPIError):
        logger.exception(f'TelegramAPIError: {exception} \nUpdate: {update}')
        return True

    logger.exception(f'Update: {update}\n{exception}')
    return True
