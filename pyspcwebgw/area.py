import logging

from pyspcwebgw.const import AreaMode
from pyspcwebgw.utils import _load_enum

_LOGGER = logging.getLogger(__name__)


class Area:
    """Represents and SPC alarm system area."""
    SUPPORTED_SIA_CODES = ('CG', 'NL', 'OG', 'BV')

    def __init__(self, gateway, spc_area):
        self._gateway = gateway
        self._id = spc_area['id']
        self._name = spc_area['name']
        self.zones = None

        self.update(spc_area)

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

    def update(self, spc_area):
        _LOGGER.debug("Update area %s", self.id)

        self._mode = _load_enum(AreaMode, spc_area['mode'])
        if self._mode == AreaMode.UNSET:
            self._last_changed_by = spc_area.get('last_unset_user_name', 'N/A')
        else:
            self._last_changed_by = spc_area.get('last_set_user_name', 'N/A')
