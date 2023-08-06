__all__ = ['setup', 'enqueue']

import argparse
import asyncio
import json
import traceback
from contextlib import asynccontextmanager
from typing import Any, Optional

import aiohttp

from . import __version__
from . import logger

WEBHOOK_METHOD: str = 'POST'
WEBHOOK_URL: Optional[str] = None
WEBHOOK_AUTH: Optional[str] = None
DEBUG = False
Messages: Optional[asyncio.Queue] = None


def setup(args: argparse.Namespace) -> bool:
    global WEBHOOK_URL, WEBHOOK_METHOD, WEBHOOK_AUTH, DEBUG, Messages

    DEBUG = args.debug

    if not args.callback_webhook_url:
        if DEBUG:
            logger.get().msg('webhooks disabled')
        return False

    WEBHOOK_URL = args.callback_webhook_url

    if args.callback_webhook_method:
        WEBHOOK_METHOD = args.callback_webhook_method.upper()

    if args.callback_webhook_auth:
        WEBHOOK_AUTH = args.callback_webhook_auth.split(':', 1)

    Messages = asyncio.Queue()

    if DEBUG:
        logger.get().msg('webhooks enabled', method=WEBHOOK_METHOD, url=WEBHOOK_URL,
            auth='enabled' if WEBHOOK_AUTH else 'disabled')
    return True


def prepare_payload(data: dict) -> None:
    data['recipients_message_to'] = json.loads(data['recipients_message_to'])
    data['recipients_message_cc'] = json.loads(data['recipients_message_cc'])
    data['recipients_message_bcc'] = json.loads(data['recipients_message_bcc'])


@asynccontextmanager
async def get_session() -> aiohttp.ClientSession:
    auth = None
    if WEBHOOK_AUTH:
        auth = aiohttp.BasicAuth(*WEBHOOK_AUTH)

    headers = {
        'User-agent': f'Sendria/{__version__} (https://github.com/msztolcman/sendria)',
        'Content-type': 'application/javascript',
    }

    session_kwargs = {
        'auth': auth,
        'headers': headers,
        'timeout': aiohttp.ClientTimeout(connect=5, total=30),
    }

    session = aiohttp.ClientSession(**session_kwargs)
    try:
        yield session
    finally:
        await session.close()


async def send_messages() -> None:
    while True:
        payload = await Messages.get()
        prepare_payload(payload)

        try:
            async with get_session() as session:
                async with session.request(WEBHOOK_METHOD, WEBHOOK_URL, json=payload) as rsp:
                    if rsp.status != 200:
                        logger.get().msg('webhook response error', message_id=payload['message_id'], status=rsp.status,
                            reason=rsp.reason, url=WEBHOOK_URL, method=WEBHOOK_METHOD)
                    elif DEBUG:
                        logger.get().msg('webhook sent', message_id=payload['message_id'], status=rsp.status,
                            reason=rsp.reason, url=WEBHOOK_URL)
        except aiohttp.ClientError:
            logger.get().msg('webhook client error', traceback=traceback.format_exc())

        Messages.task_done()


async def enqueue(msg: Any) -> None:
    if not WEBHOOK_URL:
        return

    Messages.put_nowait(msg)
