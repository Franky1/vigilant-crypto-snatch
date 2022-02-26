from typing import Optional

from .. import logger
from .logger import RemoteLogger
from .message_queue import message_queue_holder
from .message_queue import MessageQueue
from .telegram import TelegramConfig
from .telegram import TelegramSender


def add_telegram_logger(config: Optional[TelegramConfig]) -> None:
    if config:
        telegram_sender = TelegramSender(config)
        message_queue = MessageQueue(telegram_sender)
        telegram_handler = RemoteLogger(config.level, message_queue)
        message_queue_holder.set(message_queue)
        logger.addHandler(telegram_handler)
