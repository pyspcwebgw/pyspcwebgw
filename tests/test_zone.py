from pyspcwebgw import Zone
from pyspcwebgw.const import ZoneInput, ZoneStatus, ZoneType

ZONES = [{
    'id': '1',
    'type': '3',
    'zone_name': 'Kitchen smoke',
    'area': '1',
    'area_name': 'House',
    'input': '0',
    'status': '0',
}, {
    'id': '3',
    'type': '0',
    'zone_name': 'Hallway PIR',
    'area': '1',
    'area_name': 'House',
    'input': '0',
    'status': '0',
}, {
    'id': '5',
    'type': '1',
    'zone_name': 'Front door',
    'area': '1',
    'area_name': 'House',
    'input': '1',
    'status': '0',
}]


def test_parse_details():
    zone = Zone(area=None, spc_zone=ZONES[0])
    assert zone.name == 'Kitchen smoke'
    assert zone.id == '1'
    assert zone.type == ZoneType.FIRE
    assert zone.input == ZoneInput.CLOSED
    assert zone.status == ZoneStatus.OK

    zone = Zone(area=None, spc_zone=ZONES[1])
    assert zone.name == 'Hallway PIR'
    assert zone.id == '3'
    assert zone.type == ZoneType.ALARM
    assert zone.input == ZoneInput.CLOSED
    assert zone.status == ZoneStatus.OK

    zone = Zone(area=None, spc_zone=ZONES[2])
    assert zone.name == 'Front door'
    assert zone.id == '5'
    assert zone.type == ZoneType.ENTRY_EXIT
    assert zone.input == ZoneInput.OPEN
    assert zone.status == ZoneStatus.OK
