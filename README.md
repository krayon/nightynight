# NightyNight v2.0 (*NightyPyte - The MicroPython Edition*) #

[TOC]

## Introduction ##

An ESP8266 based, WS2812 night light with wifi based (web) configuration and
MQTT control.

Like PixelBall ( [Gitlab](https://gitlab.com/krayon/pixelball) /
[Github](https://github.com/krayon/pixelball) ) on steroids. Whilst PixelBall
is simple and pre-programmed, NightyNight allows for initial setup to be done
via a web interface, accessible by connecting to it, whilst it runs as a WiFi
access point. Once configured, it connects to an MQTT server and accepts
commands.

Designed as a Night Light for my Son.

# Background

Initially, NightyNight (v1) was designed around an ESP8266 running nothing but
the raw code itself. I liked it because I could write it in C and just have it
run on the hardware directly.

Unfortunately the development model for this method is slower - somewhat
similar to AVR - where you write some code, flash to test, debug etc. I was
also originally working on `ESP-01`'s and therefore didn't have much choice in
what the stack was either way due to the constraints it posed.

I eventually found the `WEMOS Mini-D1` boards ( and
[their clones](https://hackaday.com/2017/05/15/attack-on-the-clones-a-review-of-two-common-esp8266-mini-d1-boards/)
) and thought they were too good to miss. Whilst costing an extra 50%, it's
MORE than worth it considering what you get, not forgetting too that the 50%
more is a whole $1.50 (AU).

With the new board specs I could now look at heavier base. Additionally, all
the extra pins would allow for greater functionality. I don't recall how now,
but I stumbled on
[MicroPython](https://micropython.org/)
and thought it would be a good tool for the job, thus *NightyPyte* began
it's life.

## Enhancements from v1 ##

### Power Supply ###

In version 1, the ESP-01 expects 3.3v, so a power circuit needed to be used to
drop the 5v USB input power down to acceptable limits. With the Mini-D1, this
is done for us.

### Interface ###

In version 1, the interface I was designing was based around using a single
button for input, and only the coloured LED as output. With the extra pins and
an OLED screen I had laying around, I will now have an actual interface on a
screen, driven by 1, 2 or even 3 buttons.

## Installation ##

1. Download the latest
[ESP8266 build of MicroPython](http://micropython.org/download#esp8266)
image; eg. For v1.12, released 2019-12-20:

```bash
wget http://micropython.org/resources/firmware/esp8266-20191220-v1.12.bin
```

2. Erase the flash:

```bash
esptool.py --port /dev/ttyUSB0 erase_flash
```
```
esptool.py v1.2
Connecting...
Running Cesanta flasher stub...
Erasing flash (this may take a while)...
Erase took 10.2 seconds
```

3. Flash the image:

```bash
esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash -fm dio --flash_size=detect 0 esp8266-20191220-v1.12.bin
```
```
esptool.py v1.2
Connecting...
Auto-detected Flash size: 32m
Running Cesanta flasher stub...
Flash params set to 0x0240
Writing 618496 @ 0x0... 618496 (100 %)
Wrote 618496 bytes at 0x0 in 13.9 seconds (354.8 kbit/s)...
Leaving...
```

4. At this point you should be able to connect to the device via 
[picocom(8)](https://linux.die.net/man/8/picocom)
or
[screen(1)](https://linux.die.net/man/1/screen)
etc:

```bash
baud=115200; stty ispeed ${baud} ospeed ${baud} </dev/ttyUSB0 && picocom -i --baud ${baud} --imap lfcrlf /dev/ttyUSB0
```

5. Once connected, pressing <kbd>ENTER</kbd> should show the Python interactive prompt:

```
>>> 
```

6. Run the `minify.bash` script to shrink the HTML/CSS files, eg.

```bash
./minify.bash
```
```
Minifying files...
web_config_wifi.SOURCE.html (1915) --> web_config_wifi.MINIFIED.html (1212): 37% reduced
     web_reboot.SOURCE.html ( 286) -->      web_reboot.MINIFIED.html ( 266):  7% reduced
          web_nn.SOURCE.css (3944) -->           web_nn.MINIFIED.css (3280): 17% reduced
```

7. Disconnect first, then use something like
[pyboard.py](https://docs.micropython.org/en/latest/reference/pyboard.py.html)
or
[uPyLoader](https://github.com/BetaRavener/uPyLoader/)
or
[ampy](https://github.com/scientifichackers/ampy)
to transfer the *NightyNight* python files directly to the device. eg.

```bash
pyboard.py --device /dev/ttyUSB0 -f cp \
    boot.py config.json config.py index.html utils.py \
    web_config_wifi.py web_nn.css web_reboot.py webserver.py \
:
```

## Running ##

On boot of the ESP8266, the `boot.py` script will run. At present, it does the
following:

  * Check if the Button (connected to Pin 12 (D4)) is being held down;
    * If it is, enter *configuration mode*;
  * If not, check for a `config.json` file;
    * If the `config.json` file exists, but it dosen't contain non-empty
      `ssid` **AND** `pass` values, enter *configuration mode*;

  * When trying to connect to the `ssid` listed...
    * If connected successfully, enter into *normal operation* mode;
    * If connection times out, enter *configuration mode*;

Normal mode is currently just flashing the LED at a 1 second interval.

A button press in either normal mode, will break out of the `boot.py`.

## Configuration ##

In Configuration mode, the device configures itself as an Access Point (AP)
called **NightyNight-`<hexid>`-`<ip_address>`**, where:
  * `<hexid>`     - The 8 hexidecimal unique identifier for the device; and
  * `<ip_address> - The IP address that the device will be listening on, once
                    you connect.

To Configure the device, you must connect to the above access point. The
password will be **configure`<hexid>`**, where:
  * `<hexid>`     - The 8 hexidecimal unique identifier for the device.

Once connected, directing your browser to http:// `<ip_address>` to configure
the network details (SSID and Password for Access Point (AP)) as well as the
details of your MQTT server and Topic. Once these are saved, a reboot will
occur and the device will attempt to connect to the now configured AP.

At present, the MQTT details are not utilised.

[//]: # ( vim: set ts=4 sw=4 et cindent tw=80 ai si syn=markdown ft=markdown: )
