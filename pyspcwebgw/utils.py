import asyncio
import logging

import aiohttp
import async_timeout

_LOGGER = logging.getLogger(__name__)


def _load_enum(enum, value, default=None):
    """Parse an enum with fallback."""
    try:
        return enum(value)
    except ValueError:
        return default


async def async_request(session, url, **kwargs):
    """Do a web request and manage response."""
    try:
        with async_timeout.timeout(10):
            _LOGGER.debug("Sending %s to %s", kwargs, url)
            response = await session(url, **kwargs)
        if response.status != 200:
            _LOGGER.error("HTTP status %d, response %s.",
                          response.status, (await response.text()))
            return False
        result = await response.json()
    except asyncio.TimeoutError:
        _LOGGER.error("Timeout getting SPC data from %s.", url)
        return False
    except aiohttp.ClientError:
        _LOGGER.error("Error getting SPC data from %s.", url)
        return False
    else:
        _LOGGER.debug("HTTP request response: %s", result)

    if result['status'] != 'success':
        _LOGGER.error(
            "SPC Web Gateway call unsuccessful for resource: %s", url)
        return False

    return result
