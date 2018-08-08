import logging
import json
from asyncio import ensure_future

import aiohttp

_LOGGER = logging.getLogger(__name__)

STATE_STARTING = 'starting'
STATE_RUNNING = 'running'
STATE_STOPPED = 'stopped'

RETRY_TIMER = 15


class AIOWSClient:
    """Websocket transport, session handling, message generation."""
    """https://github.com/Kane610/deconz/blob/master/pydeconz/websocket.py"""

    def __init__(self, loop, session, url, async_callback):
        """Create resources for websocket communication."""
        self._loop = loop
        self._session = session
        self._url = url
        self._async_callback = async_callback
        self._data = None
        self._state = None

    @property
    def data(self):
        return self._data

    @property
    def state(self):
        """"""
        return self._state

    @state.setter
    def state(self, value):
        """"""
        self._state = value
        _LOGGER.debug('Websocket %s', value)

    def start(self):
        if self.state != STATE_RUNNING:
            self.state = STATE_STARTING
        self._loop.create_task(self.running())

    async def running(self):
        """Start websocket connection."""
        try:
            async with self._session.ws_connect(self._url) as ws:
                self.state = STATE_RUNNING
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        ensure_future(self._async_callback(
                            json.loads(msg.data)))
                        _LOGGER.debug('Websocket data: %s', msg.data)
                    elif msg.type == aiohttp.WSMsgType.CLOSED:
                        break
                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        break
        except aiohttp.ClientConnectorError:
            if self.state != STATE_STOPPED:
                self.retry()
        except Exception as err:
            _LOGGER.error('Unexpected error %s', err)
            if self.state != STATE_STOPPED:
                self.retry()
        else:
            if self.state != STATE_STOPPED:
                self.retry()

    def stop(self):
        """Close websocket connection."""
        self.state = STATE_STOPPED

    def retry(self):
        """Retry to connect to SPC."""
        self.state = STATE_STARTING
        self._loop.call_later(RETRY_TIMER, self.start)
        _LOGGER.debug('Reconnecting to SPC in %i.', RETRY_TIMER)
