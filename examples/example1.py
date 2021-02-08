import asyncio

import aiohttp
from pyspcwebgw import SpcWebGateway


API_URL = 'http://192.168.1.10:8088'
WS_URL = 'ws://192.168.1.10:8088'


async def callback(entity):
    print('SPC update - ' + str(entity))


async def init(loop):
    # logging.basicConfig(level=logging.DEBUG)

    websession = aiohttp.ClientSession(loop=loop)
    spc = SpcWebGateway(loop, websession, api_url=API_URL, ws_url=WS_URL,
                        async_callback=callback)

    result = await spc.async_load_parameters()
    if result is False:
        print('Failed to connect to SPC Web Gateway.')
        exit(1)

    # Print basic info about the panel
    print(f"Connected to SPC {spc.info['variant']}, serial no "
          f"{spc.info['sn']} running firmware {spc.info['version']}.")

    # Connect the websocket
    spc.start()

    # List and print available areas and zones
    for _, area in spc.areas.items():
        print(area)
        for zone in area.zones:
            print('   ' + str(zone))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    loop.run_until_complete(init(loop))
    loop.run_forever()
