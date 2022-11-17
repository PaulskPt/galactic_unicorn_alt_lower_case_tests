Introduction
============

This repo contains a modified example: 'GU_Workout_mod.py'.
The original by version is by Tony Goodhew - 13th Nov 2022: ´<https://forums.pimoroni.com/t/galactic-unicorn-lower-case-text/20727>


Hardware requirements
=====================

- `Pimoroni Galactic Unicorn (PIM 631)` <https://shop.pimoroni.com/products/galactic-unicorn?variant=40057440960595>
- `Adafruit AHT20 - Temperature & Humidity Sensor Breakout Board - STEMMA QT / Qwiic` <https://www.adafruit.com/product/4566>
- `Adafruit STEMMA QT / Qwiic JST SH 4-Pin Cable - 400mm long.` <https://www.adafruit.com/product/5385>
- `or Adafruit STEMMA QT / Qwiic JST SH 4-pin Cable - 100mm Long` <https://www.adafruit.com/product/4210>


Software dependencies
=============
The Pimoroni Galactic Unicorn needs the latest 'pimoroni' version of micropython .uf file:

* `pimoroni-picow_galactic_unicorn-v1.19.9-micropython.uf2` <https://github.com/pimoroni/pimoroni-pico/releases/tag/v1.19.9>

For the external ATH20 sensor you need:

* `ahtx0 module:` <https://github.com/targetblank/micropython_ahtx0/blob/master/ahtx0.py>

Added is an `experimental version` of the `ahtx0 module` (work-in-progress). 
In the `class AHT10` I added the function `e_status()` and a variable: `self._errstat`
while the functions `temperature`, `_read_to_buffer`, `_trigger_measurement` and `perform_measurement` are modified
to handle/report errors to `self._err_stat` and to `REPL`.

About this modified Example
===========================

The font definitions are moved to the file: `GU_Workout_mod_ini.py`.

Each `test` is now moved into an `own function`. 

In file: `GU_Workout_mod_ini.py`, set 'True' or 'False' the boolean variable in each list in `tests_dict` for the test you want to
include or exclude.

    `tests_dict = {
        0: ["ga",      False],  # Set to False for test you won't want to run
        1: ["rect",    False],
        2: ["tonygo2", True],
        3: ["light",   False],
        4: ["temp",    True]
    }`

This modified example contains a kinda `hotplug` algorithm for the external sensor,
using the global variable `sensor_present` and the function `reconnect_sensor()`. If, for one or other reason, the sensor gets disconnected, the script will not crash or halt. In the a case the external sensor is not connected or been disconnected, the script simply does not continue to show temperature and humidity readings. It displays a reminder to check the wiring, until the sensor has been reconnected.

The example also contains modifications to control the `brilliance` of the leds.
For this the global variable `brilliance` is used. The function `adj_val()` has been added to adjust the `r, g, b` values according to the value of 'brilliance'.

I added global boolean variable `my_debug`. Set this variable to see more output to the REPL.

Finally I added a `Reset` button (the `SLEEP` button middle, right on the board). Pressing this button will reset the microcontroller.

