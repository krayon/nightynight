# This file is executed on every boot (including wake-boot from
# deepsleep)

import uos, machine;
import gc;

gc.collect();

print("\n\n");
print("[BOOT  ] NightyNight D1 booting...");

from machine import Pin;
import time;
import network;

# GPIOs
p_but = Pin(12, Pin.IN , Pin.PULL_UP); # Button (D6)
p_led = Pin( 2, Pin.OUT);              # (Blue) Status LED (D4)

# LED init
v_led = 1; p_led.value(v_led);         # Turn the LED off

# Interfaces
w_sta = network.WLAN(network.STA_IF);
w_ap  = network.WLAN(network.AP_IF);

# Disable network for now
w_ap.active(False);

def debug_mode(): #{
    global v_led, p_but, p_led;

    print("[BOOT  ] Debug MODE: Confirmed");

    # Little flash
    v_led = 0 if v_led == 1 else 1;
    p_led.value(v_led);
    time.sleep(0.1); # 100 msec
    v_led = 0 if v_led == 1 else 1;
    p_led.value(v_led);
    time.sleep(0.1); # 100 msec
    v_led = 0 if v_led == 1 else 1;
    p_led.value(v_led);
    time.sleep(0.1); # 100 msec

    v_led = 0; p_led.value(v_led); # Turn the LED ON
    while True: #{
        time.sleep(0.5); # 500 msec
    #}
#}

# Is button pressed?
if (not p_but.value()): #{
    # Pressed
    print("[BOOT  ] Button pressed. Debug mode?");

    for i in range(1, 10): #{
        # Little flash
        v_led = 0 if v_led == 1 else 1;
        p_led.value(v_led);
        time.sleep(float(i) / 10.0); # i * 100 msec

        # Not Debug, continue boot as normal
        if (p_but.value()): break;
    #}

    # If still pressing, Debug mode
    if (not p_but.value()): #{
        # DEBUG TIME!
        debug_mode();
    #}
#}

# Normal boot here

print("[BOOT  ] Normal boot");

# vim:ts=4:tw=80:sw=4:et:ai:si
