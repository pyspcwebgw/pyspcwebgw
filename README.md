Python library for communicating with [Vanderbilt SPC alarm systems](https://vanderbiltindustries.com/spc) via the REST/websocket API provided by the SPC Web Gateway software made by [Lundix IT](http://www.lundix.se/smarta-losningar/). Using this library you can:

- Retrieve information for all alarm areas and zones.
- Change the alarm mode, i.e. arming and disarming of the alarm system.
- Get real-time updates when attributes of areas and zones change, e.g. if motion detector connected to the systems triggers or when the alarm goes off.

## Usage
### Library
To use the library in your own application see the example file.

### Stand-alone
When installing the package an interactive test shell is automatically installed. To run it:
```
spcwebgw-console <API url> <WS url>
```
Where ```<API url>```is the url of the SPC Web Gateway API and ```<WS url>``` is the url of the SPC Web Gateway websocket endpoint.

Examples of available commands in the test shell:

- ```areas```. List all available areas.
- ```zones```. List all available zones or only zones in a specific area.
- ```full_set```. Full set an area.
- ```part_set_x```. Part set x an area.
- ```unset```. Unset an area.
