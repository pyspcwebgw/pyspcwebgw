import logging

from pyspcwebgw.const import ZoneInput, ZoneType, ZoneStatus
from pyspcwebgw.utils import _load_enum

_LOGGER = logging.getLogger(__name__)


class Zone:
    """Represents an SPC alarm system zone."""
    SUPPORTED_SIA_CODES = ('ZO', 'ZC', 'ZX', 'ZD', 'ZM', 'BA',
                           'BB', 'BU', 'BR', 'BC')

    def __init__(self, area, spc_zone):
        self._id = spc_zone['id']
        self._name = spc_zone['zone_name']
        self._area = area

        self.update(spc_zone)

    def __str__(self):
        return '{id}: {name} ({type}). Input: {inp}, status: {status}'.format(
            id=self.id, name=self.name, type=self.type,
            inp=self.input, status=self.status)

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def input(self):
        return self._input

    @property
    def type(self):
        return self._type

    @property
    def status(self):
        return self._status

    @property
    def area(self):
        return self._area

    def update(self, spc_zone):
        _LOGGER.debug("Update zone %s", self.id)

        self._input = _load_enum(ZoneInput, spc_zone['input'])
        self._type = _load_enum(ZoneType, spc_zone['type'])
        self._status = _load_enum(ZoneStatus, spc_zone['status'])
