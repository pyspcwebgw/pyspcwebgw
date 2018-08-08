import logging

from pyspcwebgw.const import ZoneInput, ZoneType, ZoneStatus
from pyspcwebgw.utils import _load_enum

_LOGGER = logging.getLogger(__name__)


class Zone:
    """Represents an SPC alarm system zone."""
    SUPPORTED_SIA_CODES = ('ZO', 'ZC', 'ZX', 'ZD', 'BA')

    def __init__(self, area, spc_zone):
        self._id = spc_zone['id']
        self._name = spc_zone['zone_name']
        self._input = _load_enum(ZoneInput, spc_zone['input'])
        self._type = _load_enum(ZoneType, spc_zone['type'])
        self._status = _load_enum(ZoneStatus, spc_zone['status'])
        self._area = area

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

    def update(self, message):
        assert message['sia_address'] == self.id

        SIA_CODE_TO_STATE = {
            #       'BA': STATE_ALARM_TRIGGERED,
            'ZO': ZoneInput.OPEN,
            'ZC': ZoneInput.CLOSED,
            'ZX': ZoneInput.SHORT,
            'ZD': ZoneInput.DISCONNECTED
        }
        self._input = SIA_CODE_TO_STATE[message['sia_code']]
