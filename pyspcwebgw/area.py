import logging

from .const import AreaMode
from .utils import _load_enum

_LOGGER = logging.getLogger(__name__)


class Area:
    """Represents and SPC alarm system area."""

    SUPPORTED_SIA_CODES = ("CG", "NL", "OG", "BV")

    def __init__(self, gateway, spc_area):
        self._gateway = gateway
        self._id = spc_area["id"]
        self._name = spc_area["name"]
        self._verified_alarm = False
        self.zones = None

        self.update(spc_area)

    def __str__(self):
        return "{id}: {name}. Mode: {mode}, last changed by {last}.".format(
            name=self.name, id=self.id, mode=self.mode, last=self.last_changed_by
        )

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def verified_alarm(self):
        return self._verified_alarm

    @property
    def mode(self):
        return self._mode

    @property
    def last_changed_by(self):
        return self._last_changed_by

    def update(self, spc_area, sia_code=None, sia_description=None):
        _LOGGER.debug("Update area %s", self.id)

        self._mode = _load_enum(AreaMode, spc_area["mode"])
        self._verified_alarm = sia_code == "BV"
        if self._mode == AreaMode.UNSET:
            self._last_changed_by = spc_area.get("last_unset_user_name", "N/A")
        elif self._mode == AreaMode.FULL_SET:
            self._last_changed_by = spc_area.get("last_set_user_name", "N/A")
        # If PART_SET, last_changed_by user is not provided by the EDP protocol.
        # We can instead get the last_changed_by user from the second part of the sia_description.
        # sia_description should in this case contain "Area_name¦User_name¦User_ID".
        # Added check so SIA description has expected length 3,
        # since there is no user if a "shortcut button" is used for arming.
        elif sia_code == "NL" and len(sia_description.split("¦")) == 3:
            self._last_changed_by = sia_description.split("¦")[1]
        else:
            self._last_changed_by = "N/A"
