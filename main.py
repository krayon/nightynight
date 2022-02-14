# Normal mode

import os, machine;
import gc;

gc.collect();

print("\n\n");
print("[MAIN  ] Normal boot");

from machine import Pin;
import time;
import network;
import config;

# GPIOs
p_but = Pin(12, Pin.IN , Pin.PULL_UP); # Button (D6)
p_led = Pin( 2, Pin.OUT);              # (Blue) Status LED (D4)

# LED init
v_led = 1; p_led.value(v_led);         # Turn the LED off

while True: #{
    v_led = 0 if v_led == 1 else 1;
    p_led.value(v_led);
    print("[LOOP  ] LED (" + str(v_led) + ")");
    time.sleep(1); # 1 sec

    # Button breaks out of loop
    if (not p_but.value()): break;
#}

# vim:ts=4:tw=80:sw=4:et:ai:si
