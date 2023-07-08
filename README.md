# WING LED
Hi I made this API to run WS2818 LEDs through my wings, but I thought that the API would be robust enough to handle multiple strips of 2818 LEDs with varying lengths.
This was created originally to run on a rhaspberry pi pico W

## SETUP

### LED strip configuration
Each LED strip will be connected by data to a different pin from your rhaspberry pi.  In order to configure this, you will have to open and manipulate the CONSTANTS file.
Near the bottom of the file, you will see a MachineSetupConstants.  In which, there is a definition for LINES = []
You may add one tuple for each LED strip you want to control.  The tuple will be of this form ( DATA_PIN, COUNT, BRIGHTNESS )
 DATA_PIN will coorespond to which pin on your pi this LED strip will connect to.
 COUNT will be the number of LEDs are on the strip to be controlled.
 BRIGHTNESS is a global max brightness setting that the lights on that strip should never exceed, between 0 and 1

### WIFI configuration
In order to connect to your pi and use the API, you will have to be able to connect to wifi.  To configure this, again look into the CONSTANTS file.  Within it, you will see a WifiConstants.  Here you may enter in your own SSID (Name of your wifi) and PASSWORD to that wifi.
You will have to find the IP assigned to the pi and enter that into the HOST variable.  192.168.1.222 is the default given, that happened to be what I was assigned.
I'm running this on port 80 so its http by default, but any port will be OK if you want..

### UPDATE FREQUENCY
LEDs are kept in sync globally VIA a heart beat.  The machine will do all of the calculations to figure out what colors need to be shown next for each LED, and then sleep until a heart beat occurs.  Once a heart beat is signaled, the machine will awaken to update the strips, and then figure out what the next colors should be over and over again.
The frequency of the heart beat is a configuration in the CONSTANTS file called FREQUENCY.  This value refers to the number of heart beats that will occur in one minute.  I've defaulted this to 600, as in 10 color updates may happen per second for each LED.

## API

### Pattern
From the top down, our program is built on Wings.  The wings have many strips of LEDs, and the LED strips have LEDs, and each LED is assigned an update strategy that controls when and how the light should update.

### GET /
Index.  This should post the starting HTML page that will start the app.

### GET /strips
Get strips data.  This will return a list of all of the LED strips that are currently configured.

| property       | data type  | description |
| -------------- | ---------- | ---------------------------------------------------------------------------- |
| count          | integer    | The number of strips that have been configured and are successfully running. |
| strips         | array      | An array of strip objects. |
| strips.lights  | integer    | The count of lights on the strip |
| strips.self    | string     | A URL link to the strip |

### GET /strips/{id}
Get data from a single strip.  The id will be an integer matching the index of the strip in the configuration array.  This will return a list of lights that belong to the current strip.

| property       | data type  | description |
| -------------- | ---------- | ---------------------------------------------------------------------------- |
| count          | integer    | The number of LEDs that are running on the current strip.. |
| lights         | array      | An array of light objects, represneting each LED. |
| lights.self    | string     | A URL link to the light. |

### GET /strips/{id}/lights/{lightId}
Get data from a single light.  This id will be the strip index.  The lightId will be the index of the light in the strip.  This will return the current configuration of the light.

| property       | data type  | description |
| -------------- | ---------- | ---------------------------------------------------------------------------- |
| strip          | integer    | The index of the strip this light exists on. |
| position       | integer    | The position of this light (Should match lightId) |
| hue            | integer    | A number between 0 and 360 representing the hue of the color. |
| saturation     | decimal    | A decimal between 0 and 1 representing how saturated the color will be. |
| value          | decimal    | A number between 0 and 1 representing how dark or light the color will be. |
| updateStrategy | object     | The current strategy that the light uses to decide when \ how to update color. |
| us.updateFrequency | integer| The frequency that the LED will update.  Every n heartbeats will result in a new color. |
| us.type        | enum       | strategy name.  Can be Null, Fade, Jump, or Wheel |
| us.updateOffset| integer    | Offset from the heart beat.  If frequency = 5, we update on the 5th, 10th, 15th, and so on heart beat.  With the offset = 1, we update on the 6th, 11th, 16th and so on heart beat. |
| us.colors      | array      | An array of colors for the strategies to shift between |