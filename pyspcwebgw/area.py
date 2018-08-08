import logging

from pyspcwebgw.const import AreaMode
from pyspcwebgw.utils import _load_enum

_LOGGER = logging.getLogger(__name__)


class Area:
    """Represents and SPC alarm system area."""
    SUPPORTED_SIA_CODES = ('CG', 'NL', 'OG')

    def __init__(self, gateway, spc_area):
        self._gateway = gateway
        self._id = spc_area['id']
        self._name = spc_area['name']
        self._mode = _load_enum(AreaMode, spc_area['mode'])
        if self._mode == AreaMode.UNSET:
            self._last_changed_by = spc_area.get('last_unset_user_name', 'N/A')
        else:
            self._last_changed_by = spc_area.get('last_set_user_name', 'N/A')
        self.zones = None

    def __str__(self):
        return '{id}: {name}. Mode: {mode}, last changed by {last}.'.format(
            name=self.name, id=self.id,
            mode=self.mode, last=self.last_changed_by)

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def mode(self):
        return self._mode

    @property
    def last_changed_by(self):
        return self._last_changed_by

    def update(self, message):
        _LOGGER.debug("Update area %s", self.id)

        if 'description' in message:
            data = message['description'].split('¦')
            if len(data) == 3:
                self._last_changed_by = data[1]

        SIA_CODE_TO_MODE = {
            'CG': AreaMode.FULL_SET,
            'NL': AreaMode.PART_SET_A,
            'OG': AreaMode.UNSET
        }
        self._mode = SIA_CODE_TO_MODE[message['sia_code']]
