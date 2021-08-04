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
    retry = -1
    retries = 25
    while True:
        retry += 1
        if retry > 0:
            delay = float(retry * retry) / 10.0
            _LOGGER.info('Sleeping %0.2f seconds for exponential backoff', delay)
            await asyncio.sleep(delay)
        try:
            with async_timeout.timeout(20):
                _LOGGER.debug("Sending %s to %s", kwargs, url)
                response = await session(url, **kwargs)
        except (aiohttp.ClientError, asyncio.TimeoutError) as err:
            if retry < retries:
                _LOGGER.warning('Retrying', err)
                continue
            return False
        except ValueError as err:
            _LOGGER.warning('ValueError from aiohttp: redirect to non-http or https', err)
            raise False
        except RuntimeError as err:
            _LOGGER.warn('RuntimeError from aiohttp: session closed', err)
            raise False
        # Handle non 2xx status code and retry if possible
        if 500 <= response.status < 600 and retry < retries:
            if retry < retries:
                _LOGGER.warning('Retrying because of: %d status' % response.status)
                continue
            else:
                _LOGGER.error("HTTP status %d, response %s.",
                              response.status, (await response.text()))
                return False
        result = await response.json()

        if result['status'] != 'success':
            _LOGGER.error(
                "SPC Web Gateway call unsuccessful for resource: %s", url)
            return False
        return result
