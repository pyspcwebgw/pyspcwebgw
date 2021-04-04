"""Tests for Vanderbilt SPC component."""
import asyncio

import aiohttp
import pytest
from aioresponses import aioresponses
from aioresponses.compat import URL

from pyspcwebgw import SpcWebGateway, Area, Zone
from pyspcwebgw.const import AreaMode, ZoneInput


info = """{"status":"success","data":{"panel":{"cfgtime": "1593425759",
    "device-id": "1", "hw_ver_major": "1",
    "hw_ver_minor": "4", "hw_ver_vds": "0", "license_key": "ABC123", "sn":
    "DEADBEEF", "type": "SPC4000", "variant": "4300",
    "version": "3.8.5 - R.31629"}}}"""

areas = """{"status":"success","data":{"area":[{"id":"1","name":"House",
    "mode":"0","last_set_time":"1485759851","last_set_user_id":"1",
    "last_set_user_name":"Pelle","last_unset_time":"1485800564",
    "last_unset_user_id":"1","last_unset_user_name":"Pelle","last_alarm":
    "1478174896"},{"id":"3","name":"Garage","mode":"0","last_set_time":
    "1483705803","last_set_user_id":"9998","last_set_user_name":"Lisa",
    "last_unset_time":"1483705808","last_unset_user_id":"9998",
    "last_unset_user_name":"Lisa"}]}}"""

area_update = """{"status":"success","data":{"area":[{"id":"1","name":"Huset",
    "mode":"3","last_set_time":"1534431659","last_set_user_id":"9998",
    "last_set_user_name":"Lisa","last_unset_time":"1534435693",
    "last_unset_user_id":"1","last_unset_user_name":"Pelle",
    "last_alarm":"1534372056","not_ready_set":"1011"}]}}"""

area_update_2 = """{"status":"success","data":{"area":[{"id":"1","name":"Garage",
    "mode":"1","last_set_time":"1534431659","last_set_user_id":"9998",
    "last_set_user_name":"Lisa","last_unset_time":"1534435693",
    "last_unset_user_id":"1","last_unset_user_name":"Pelle",
    "last_alarm":"1534372056","not_ready_set":"1011"}]}}"""

zones = """{"status":"success","data":{"zone":[{"id":"1","type":"3",
    "zone_name":"Kitchen smoke","area":"1","area_name":"House","input":"0",
    "logic_input":"0","status":"0","proc_state":"0","inhibit_allowed":"1",
    "isolate_allowed":"1"},{"id":"3","type":"0","zone_name":"Garage PIR",
    "area":"3","area_name":"Garage","input":"0","logic_input":"0","status":
    "0","proc_state":"0","inhibit_allowed":"1","isolate_allowed":"1"},
    {"id":"4","type":"0","zone_name":"Garage door","area":"3",
    "area_name":"Garage","input":"0","logic_input":"0","status":
    "0","proc_state":"0","inhibit_allowed":"1","isolate_allowed":"1"},
    {"id":"5","type":"1","zone_name":"Front door","area":"1","area_name":
    "House","input":"1","logic_input":"0","status":"0","proc_state":"0",
    "inhibit_allowed":"1","isolate_allowed":"1"}]}}"""

zone_update = """{"status":"success","data":{"zone":{"id":"3","type":"0",
    "zone_name":"Garage PIR","area":"3","area_name":"Garage","input":"1",
    "logic_input":"0","status":"0","proc_state":"0","inhibit_allowed":"1",
    "isolate_allowed":"1"}}}"""

zone_update_closed = """{"status":"success","data":{"zone":{"id":"3","type":"0",
    "zone_name":"Garage PIR","area":"3","area_name":"Garage","input":"0",
    "logic_input":"0","status":"0","proc_state":"0","inhibit_allowed":"1",
    "isolate_allowed":"1"}}}"""


@pytest.fixture
async def session():
    async with aiohttp.ClientSession() as session:
        yield session


@pytest.fixture
async def spc(event_loop, session):
    class SpcAndResponseMock:
        def __init__(self, spc, mock):
            self.spc = spc
            self.mock = mock

    """HTTP client mock for areas and zones."""
    with aioresponses() as m:
        m.get('http://localhost/spc/panel', body=info)
        m.get('http://localhost/spc/area', body=areas)
        m.get('http://localhost/spc/area/1', body=area_update)
        m.get('http://localhost/spc/area/3', body=area_update_2)
        m.get('http://localhost/spc/zone', body=zones)
        m.get('http://localhost/spc/zone/3', body=zone_update)
        m.get('http://localhost/spc/zone/4', body=zone_update_closed)
        m.put('http://localhost/spc/area/1/set',
              payload={'status': 'success'})
        m.put('http://localhost/spc/area/1/unset',
              payload={'status': 'success'})
        m.put('http://localhost/spc/area/1/set_a',
              payload={'status': 'success'})
        m.put('http://localhost/spc/area/1/set_b',
              payload={'status': 'success'})

        spc = SpcWebGateway(event_loop, session,
                            'http://localhost/',
                            'ws://localhost/', None)

        await spc.async_load_parameters()
        yield SpcAndResponseMock(spc, m)


def test_parse_areas(spc):
    assert len(spc.spc.areas) == 2
    assert spc.spc.areas['1'].name == 'House'
    assert spc.spc.areas['3'].name == 'Garage'


def test_parse_area_zones(spc):
    assert len(spc.spc.areas['1'].zones) == 2
    assert len(spc.spc.areas['3'].zones) == 2


@pytest.mark.asyncio
async def test_area_mode_update_callback(spc, event_loop):
    async def callback(entity):
        if not isinstance(entity, Area) or entity.mode != AreaMode.FULL_SET:
            pytest.fail('invalid entity in callback')

    msg = {'data': {'sia': {'sia_code': 'CG', 'sia_address': '1'}}}
    assert spc.spc.areas['1'].mode == AreaMode.UNSET
    spc.spc._async_callback = callback
    tasks = await spc.spc._async_ws_handler(data=msg)
    assert ('GET', URL('http://localhost/spc/area/1')) in spc.mock.requests
    await asyncio.gather(*tasks)


@pytest.mark.asyncio
async def test_alternate_area_mode_update_callback(spc, event_loop):
    async def callback(entity):
        if not isinstance(entity, Area):
            pytest.fail('invalid entity in callback')
        if entity.id == '1' and entity.mode != AreaMode.FULL_SET:
            pytest.fail("Entity data does not match expectation")
        if entity.id == '3' and entity.mode != AreaMode.PART_SET_A:
            pytest.fail("Entity data does not match expectation")

    msg = {'data': {'sia': {'sia_code': 'CL', 'sia_address': '9999'}}}
    spc.spc._async_callback = callback
    tasks = await spc.spc._async_ws_handler(data=msg)
    assert ('GET', URL('http://localhost/spc/area/1')) in spc.mock.requests
    assert ('GET', URL('http://localhost/spc/area/3')) in spc.mock.requests
    await asyncio.gather(*tasks)


@pytest.mark.asyncio
async def test_area_alarm_triggered(spc, event_loop):
    async def callback(entity):
        if not isinstance(entity, Area) or not entity.verified_alarm:
            pytest.fail('invalid entity in callback')

    msg = {'data': {'sia': {'sia_code': 'BV', 'sia_address': '1'}}}
    assert not spc.spc.areas['1'].verified_alarm
    spc.spc._async_callback = callback
    tasks = await spc.spc._async_ws_handler(data=msg)
    await asyncio.gather(*tasks)


@pytest.mark.asyncio
async def test_zone_input_update_callback(spc, event_loop):
    async def callback(entity):
        if not isinstance(entity, Zone) or entity.input != ZoneInput.OPEN:
            pytest.fail('invalid entity in callback')

    msg = {'data': {'sia': {'sia_code': 'ZO', 'sia_address': '3'}}}
    assert spc.spc.areas['3'].zones[0].input == ZoneInput.CLOSED
    spc.spc._async_callback = callback
    tasks = await spc.spc._async_ws_handler(data=msg)
    assert ('GET', URL('http://localhost/spc/zone/3')) in spc.mock.requests
    await asyncio.gather(*tasks)


@pytest.mark.asyncio
@pytest.mark.parametrize("url_part,mode", [
    ('set', AreaMode.FULL_SET),
    ('unset', AreaMode.UNSET),
    ('set_a', AreaMode.PART_SET_A),
    ('set_b', AreaMode.PART_SET_B)
])
async def test_change_area_mode(spc, url_part, mode):
    await spc.spc.change_mode(spc.spc.areas['1'], mode)
    url = 'http://localhost/spc/area/1/{}'.format(url_part)
    assert ('PUT', URL(url)) in spc.mock.requests


@pytest.mark.asyncio
async def test_pir_workaround(spc, event_loop):
    async def callback(entity):
        if not isinstance(entity, Zone) or entity.input != ZoneInput.OPEN:
            pytest.fail('invalid entity in callback')

    msg = {'data': {'sia': {'sia_code': 'ZO', 'sia_address': '4', 'input': '0'}}}
    assert spc.spc.areas['3'].zones[1].input == ZoneInput.CLOSED
    spc.spc._async_callback = callback
    tasks = await spc.spc._async_ws_handler(data=msg)
    assert ('GET', URL('http://localhost/spc/zone/4')) in spc.mock.requests
    await asyncio.gather(*tasks)
