Python library for communicating with [Vanderbilt SPC alarm systems](https://vanderbiltindustries.com/spc) via the REST/websocket API provided by the SPC Web Gateway software made by [Lundix IT](http://www.lundix.se/smarta-losningar/). Using this library you can:

- Retrieve information for all alarm areas and zones.
- Change the alarm mode, i.e. arming and disarming of the alarm system.
- Get real-time updates when attributes of areas and zones change, e.g. if motion detector connected to the systems triggers or when the alarm goes off.

## Usage

### Library

- ```areas```. List all available areas.
- ```zones```. List all available zones or only zones in a specific area.
- ```full_set```. Full set an area.
- ```part_set_x```. Part set x an area.
- ```unset```. Unset an area.
- ```debug```. Toggle debug output.

## Flex Gateway

While initially written for SPC Web Gateway you can use this for SPC Flex Gateway as well.

There is a (big!) security caveat though, you can't enable login for `get_user` in the Flex Gateway `config.xml`.

=======
To use the library in your own application see the example file.
