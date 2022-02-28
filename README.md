# NightyNight v2 (*NightyPyte - The MicroPython Edition*) #

[TOC]

# Introduction #

An ESP8266 based, WS2812 night light with wifi based (web) configuration and
MQTT control.

Like PixelBall ( [Gitlab](https://gitlab.com/krayon/pixelball) /
[Github](https://github.com/krayon/pixelball) ) on steroids. Whilst PixelBall
is simple and pre-programmed, NightyNight allows for initial setup to be done
via a web interface, accessible by connecting to it, whilst it runs as a WiFi
access point. Once configured, it connects to an MQTT server and accepts
commands.

Designed as a Night Light for my Son.

# Background #

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

# Enhancements from v1 #

## Power Supply ##

In version 1, the ESP-01 expects 3.3v, so a power circuit needed to be used to
drop the 5v USB input power down to acceptable limits. With the Mini-D1, this
is done for us.

## Interface ##

In version 1, the interface I was designing was based around using a single
button for input, and only the coloured LED as output. With the extra pins and
an OLED screen I had laying around, I will now have an actual interface on a
screen, driven by 1, 2 or even 3 buttons.

# Installation #

1. Download the latest
[ESP8266 build of MicroPython](http://micropython.org/download#esp8266)
image; eg. For v1.18, released 2022-01-17:

```bash
wget https://micropython.org/resources/firmware/esp8266-20220117-v1.18.bin
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
esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash -fm dio --flash_size=detect 0 esp8266-20220117-v1.18.bin
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
baud=115200
stty \
    ispeed ${baud}  \
    ospeed ${baud}  \
    min          1  \
    time        10  \
    -icrnl -onlcr   \
    -opost -isig    \
    -icanon -iexten \
    -echo -echoe    \
    -echok -echoctl \
    -echoke         \
</dev/ttyUSB0 && picocom -i --baud ${baud} --imap lfcrlf /dev/ttyUSB0
```

5. Once connected, pressing <kbd>ENTER</kbd> should show the Python interactive prompt:

```
>>>
```

6. Disconnect.

7. If you don't have your own config yet, create one:

```bash
cp -ai config.json{.TEMPLATE,}
```

7. Run the `minify.bash` script to shrink the HTML/CSS files, eg.

```bash
./minify.bash
```
```
Minifying files...
          web_nn.SOURCE.css (3944) -->           web_nn.MINIFIED.css (3280): 17% reduced
```

8. Use something like
[pyboard.py](https://docs.micropython.org/en/latest/reference/pyboard.py.html)
or
[uPyLoader](https://github.com/BetaRavener/uPyLoader/)
or
[ampy](https://github.com/scientifichackers/ampy)
to transfer the *NightyNight* python files directly to the device. eg.

```bash
pyboard.py --device /dev/ttyUSB0 -f cp \
    config.json app.py globs.py ui.py utils.py \
    debug.py config.py main.py boot.py \
    web_server.py web_pyhtml.py web_nn.css \
    index.py index.pyhtml \
    web_reboot.py web_reboot.pyhtml \
    web_config_wifi.py web_config_wifi.pyhtml \
    favicon.ico favicon.16x16.png favicon.32x32.png \
:
```

  - _don't forget the `:` at the end there - it's the destination (the device)_

# Running #

On boot of the ESP8266, **_Boot_** (`boot.py`) script will run.

## Boot ##

`boot.py` does the following:

  * Turns off wifi;
  * Turns off blue status LED (connected to Pin 2 (D4);
  * Check if the Button (connected to Pin 12 (D6)) is being held down;
  * If button is held:
    * Start flashing at increasing speed;
    * If still held after 8 "rounds":
      * Set `globs.mode` to `MODE_DEBUG`
      * GOTO **_Debug Mode_**;
    * If NOT still held after 8 "rounds":
      * Set `globs.mode` to `MODE_CONFIG`
  * Load configuration (from `config.json`);
  * If config contains valid wifi settings:
    * Turn on wifi client and try to connect;
  * If config does NOT contain valid wifi settings:
    * Set `globs.mode` to `MODE_CONFIG`
  * If we did not connect successfully:
    * Configure own Access Point (AP);
    * Set `globs.mode` to `MODE_CONFIG`
  * Run **_Main_** (`main.py`)

## Main ##

`main.py` does the following:

  * Checks the `globs.mode` variable and routes to either:
    * `MODE_CONFIG`: **_Config Mode_** (`config.py:config.launch_app()`)
    * `MODE_APP`:    **_App    Mode_** (`app.py`)

## App Mode ##

`app.py` does the following:

  * Turns the blue status LED on  when the button is     pressed;
  * Turns the blue status LED off when the button is not pressed;

## Config Mode ##

In certain cases, **_Config Mode_** (`config.launch_app()`) can be activated.

### Network ###

**_Config Mode_** can be entered when either connected to an existing network,
or when running it's own Access Point (AP). The AP will run when either:

  1. The connection failed in some way (timed out, password wrong, AP not found
     etc); or
  2. Or, the user selected **_Config Mode_** (by holding the button down on boot
     for _less than_ 8 seconds) and then selected own AP (by pressing the button
     during the connection (increased pulsing LED) phase).

#### Own AP ####

##### ESSID #####

When running its own AP, the device sets its SSID to
"**NightyNight-`<hexid>`-`<ip_address>`**", where:

  * `<hexid>`      - The 8 hexidecimal unique identifier for the device; and
  * `<ip_address>` - The IP address that the device will be listening on, once
                     you connect to it.

##### Password #####

The password for this AP will be "**configure`<hexid>`**", where:

  * `<hexid>`     - The 8 hexidecimal unique identifier for the device.

### Configuration ###

Once in **_Config Mode_**, you can connect to the device's AP (if applicable)
then direct your browser to `http://<ip_address>` to configure the device.

Configurable options are:

  * Network details
    * SSID
    * Password
  * MQTT details
    * MQTT Server
    * MQTT Port
    * MQTT Topic

Once these are saved, a reboot will occur.

## Debug Mode ##

In certain cases, **_Debug Mode_** (`debug_mode()`) can be activated.

**_Debug Mode_** does the following:

  * Turns on blue status LED
  * Launches the REPL interface (on UART 0)

# Design Decisions #

## pyhtml ##

The reason I seemingly overengineered a html templatey thing is mainly due to
the ESP8266's (well, D1 Mini really) memory limitations. With very limited
memory, even a basic page couldn't easily be stored as a string in a module and
served. Once I knew I had to stream them off "disk", I figured I'd add a way to
easily insert variables within the content. Good idea? Dunno yet but it works :)

[//]: # ( vim: set ts=4 sw=4 et cindent tw=80 ai si syn=markdown ft=markdown: )
