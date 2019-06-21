# MiniTron

MiniTron is a miniature jumbotron interface built for Raspberry Pi 3-compatible LED displays. It pulls data from a custom API using a web sraper to scrape game data from [Baseball-Reference](https://baseball-reference.com). Data displayed is currently the teams and scores plus wins/losses/saves for pitchers.


## Required Hardware

I recommend using products from Adafruit as that is where I sourced the hardware. Other sources may not be compatible with MiniTron.

* **Raspberry Pi Model 3** -- *2 will most likely work but is untested*
* **LED board**
* **[Adafruit RGB Matrix HAT](https://www.adafruit.com/product/2345)**
* **5V, 2A OR 4A Power cable for LED board** -- *Optional, but recommended to avoid overloading the Pi's power supply*


## Current Limitations

The original version of MiniTron only gives consideration to LED screens consisting of a single 64x64 panel. Exact specifications of the panel I used can be found on Adafruit [here](https://www.adafruit.com/product/3649).

The Adafruit HAT does require soldering connectors to the board. The LED matrix I used also requires additional soldering of a jumper pad to enable 64x64 display. You can find installation instructions for the HAT [here](https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi/assembly). You will need to follow instructions to assemble the HAT specifically for your display.

MiniTron is only capable of displaying game data one day before the current date. This is a restriction from MLB requiring paid access to real-time data.

## Installation

**Step 1.** -- Assemble Hardware

Assemble the HAT and LED matrix according to manufacturer specifications. You can find HAT assembly instructions [here](https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi/assembly), and the LED panel I used required little assembly.

**Step 2.** -- Download Required Dependencies

MiniTron requires an RGB matrix library from [Henner Zeller](https://github.com/hzeller/rpi-rgb-led-matrix) to drive the display. Install it from the terminal on the Pi:

```
curl https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/rgb-matrix.sh >rgb-matrix.sh

sudo bash rgb-matrix.sh
```

According to installation instructions for the HAT, you will want to select Option 2 for the interface board type and Option 1 for Quality, following instructions for soldering for that option.

At this point you can test samples from 

```
rpi-rgb-led-matrix/bindings/python/samples/
```

using

```
sudo ./{SAMPLE_FILE_NAME}.py --led-rows={MATRIX_WIDTH} --led-rows={MATRIX_HEIGHT}
```

A full list of commannd line arguments can be found [here](https://github.com/hzeller/rpi-rgb-led-matrix#changing-parameters-via-command-line-flags)

**Step 3.** Fork Repo and Run!

Fork the repo, navigate to the project folder, and use 

```
sudo ./baseball.py --led-rows=64 --led-cols=64
```

to run MiniTron on a 64x64 display.

## Contributing

* Feel free to submit a PR, or open an issue! Currently it would be very helpful to test the display on other matrix sizes!