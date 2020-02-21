# NightyNight v2.0 (*NightyPyte - The MicroPython Edition*)

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
but I stumbled on MicroPython and thought it would be a good tool for the job,
thus *NightyPyte* began it's life.

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

