"""Python wrapper for the Lundix SPC Web Gateway REST API."""
import logging
from urllib.parse import urljoin
from asyncio import ensure_future

from .area import Area
from .zone import Zone
from .const import AreaMode
from .utils import async_request
from .websocket import AIOWSClient

_LOGGER = logging.getLogger(__name__)


class SpcWebGateway:
    """Alarm system representation."""

    def __init__(self, loop, session, api_url, ws_url, async_callback):
        """Initialize the client."""
        self._loop = loop
        self._session = session
        self._api_url = api_url
        self._ws_url = ws_url
        self._areas = {}
        self._zones = {}
        self._websocket = None
        self._async_callback = async_callback

    @property
    def areas(self):
        """Retrieve all available areas."""
        return self._areas

    def start(self):
        """Connect websocket to SPC Web Gateway."""
        self._websocket = AIOWSClient(loop=self._loop,
                                      session=self._session,
                                      url=self._ws_url,
                                      async_callback=self._async_ws_handler)
        self._websocket.start()

    async def async_load_parameters(self):
        """Fetch area and zone info from SPC to initialize."""
        zones = await self._async_get_data('zone')
        areas = await self._async_get_data('area')
        if not zones or not areas:
            return False
        self._load_parameters(areas, zones)

    async def change_mode(self, area, new_mode):
        """Set/unset/part set an area."""
        if not isinstance(new_mode, AreaMode):
            raise TypeError("new_mode must be an AreaMode")

        AREA_MODE_COMMAND_MAP = {
            AreaMode.UNSET: 'unset',
            AreaMode.PART_SET_A: 'set_a',
            AreaMode.PART_SET_B: 'set_b',
            AreaMode.FULL_SET: 'set'
        }
        url = urljoin(self._api_url, "spc/area/{area_id}/{command}".format(
            area_id=area.id, command=AREA_MODE_COMMAND_MAP[new_mode]))

        return await async_request(self._session.put, url)

    def _load_parameters(self, areas, zones):
        """Populate zone and area collections."""
        for spc_area in areas:
            area = Area(self, spc_area)
            area_zones = [Zone(area, z) for z in zones
                          if z['area'] == spc_area['id']]
            area.zones = area_zones
            self._areas[area.id] = area
            self._zones.update({z.id: z for z in area_zones})

    async def _async_ws_handler(self, data):
        """Process incoming websocket message."""
        sia_message = data['data']['sia']
        spc_id = sia_message['sia_address']
        sia_code = sia_message['sia_code']

        _LOGGER.debug("SIA code is %s for ID %s", sia_code, spc_id)

        if sia_code in Area.SUPPORTED_SIA_CODES:
            entity = self._areas[spc_id]
        elif sia_code in Zone.SUPPORTED_SIA_CODES:
            entity = self._zones[spc_id]
        else:
            _LOGGER.error("Update for unregistered area/zone ID %s.", spc_id)
            return
        entity.update(sia_message)
        if self._async_callback:
            ensure_future(self._async_callback(entity))

    async def _async_get_data(self, resource):
        """Get the data from the resource."""
        url = urljoin(self._api_url, "spc/{}".format(resource))
        data = await async_request(self._session.get, url)
        if not data:
            return False
        return [item for item in data['data'][resource]]
