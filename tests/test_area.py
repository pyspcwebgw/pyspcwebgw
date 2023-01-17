from pyspcwebgw import Area
from pyspcwebgw.const import AreaMode

AREA_DEF_1 = {
    "id": "1",
    "name": "House",
    "mode": "3",
    "last_set_time": "1485759851",
    "last_set_user_id": "1",
    "last_set_user_name": "Pelle",
    "last_unset_time": "1485800564",
    "last_unset_user_id": "1",
    "last_unset_user_name": "Lisa",
    "last_alarm": "1478174896",
}

AREA_DEF_2 = {
    "id": "3",
    "name": "Garage",
    "mode": "0",
    "last_set_time": "1483705803",
    "last_set_user_id": "9998",
    "last_set_user_name": "Pelle",
    "last_unset_time": "1483705808",
    "last_unset_user_id": "9998",
    "last_unset_user_name": "Lisa",
}


def test_parse_details():
    area = Area(gateway=None, spc_area=AREA_DEF_1)
    assert area.name == "House"
    assert area.mode == AreaMode.FULL_SET

    area = Area(gateway=None, spc_area=AREA_DEF_2)
    assert area.name == "Garage"
    assert area.mode == AreaMode.UNSET


def test_last_changed_by_depends_on_mode():
    area = Area(gateway=None, spc_area=AREA_DEF_1)
    assert area.last_changed_by == "Pelle"

    area = Area(gateway=None, spc_area=AREA_DEF_2)
    assert area.last_changed_by == "Lisa"
