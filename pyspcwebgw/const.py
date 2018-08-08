from enum import Enum


class AreaMode(Enum):
    UNSET = '0'
    PART_SET_A = '1'
    PART_SET_B = '2'
    FULL_SET = '3'


class ZoneInput(Enum):
    CLOSED = '0'
    OPEN = '1'
    SHORT = '2'
    DISCONNECTED = '3'
    PIRMASKED = '4'
    DC_SUBSTITUTION = '5'
    SENSOR_MISSING = '6'
    OFFLINE = '7'


class ZoneType(Enum):
    ALARM = '0'
    ENTRY_EXIT = '1'
    EXIT_TERMINATOR = '2'
    FIRE = '3'
    FIRE_EXIT = '4'
    LINE = '5'
    PANIC = '6'
    HOLD_UP = '7'
    TAMPER = '8'
    TECHNICAL = '9'
    MEDICAL = '10'
    KEYARM = '11'
    UNUSED = '12'
    SHUNT = '13'
    X_SHUNT = '14'
    FAULT = '15'
    LOCK_SUPERVISION = '16'
    SEISMIC = '17'
    ALL_OKAY = '18'


class ZoneStatus(Enum):
    OK = '0'
    INHIBIT = '1'
    ISOLATE = '2'
    SOAK = '3'
    TAMPER = '4'
    ALARM = '5'
    OK_NOT_RECENT = '6'
    TROUBLE = '7'
