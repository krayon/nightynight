# This file is executed on every boot (including wake-boot from
# deepsleep)

import os, machine;
import gc;

gc.collect();

print("\n\n");
print("[BOOT  ] NightyNight D1 booting...");

from machine import Pin;
import time;
import network;
import config;

# GPIOs
p_but = Pin(12, Pin.IN , Pin.PULL_UP); # Button (D6)
p_led = Pin( 2, Pin.OUT);              # (Blue) Status LED (D4)

# LED init
v_led = 1; p_led.value(v_led);         # Turn the LED off

# Interfaces
w_sta = network.WLAN(network.STA_IF);
w_ap  = network.WLAN(network.AP_IF);

# Disable network for now
w_sta.active(False);
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

# Network timeout in ms
timeout_net_ms = 30000;

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

        #HARD# # Soft reset
        #HARD# import sys;
        #HARD# sys.exit();

        # Hard reset
        import machine;
        machine.reset();
    #}
#}

# Normal boot here

v_led = 1; p_led.value(v_led);        # Turn the LED off

# Load Configuration
if (config): #{
    print("[BOOT  ] Loading configuration...");
    config.config_load();

    if (
        config.config
        and 'ssid' in config.config
        and len(config.config['ssid']) > 0
        and 'pass' in config.config
        and len(config.config['pass']) > 0
    ): #{
        print("[BOOT  ] Existing AP ("
        + config.config['ssid']
        + ") configured, connecting...");

        w_sta.active(True);
        w_sta.connect(config.config['ssid'], config.config['pass']);

        start = time.ticks_ms();
        delta = 0;
        while (delta < timeout_net_ms): #{



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



            time.sleep(0.7); # 700 msec
            delta = time.ticks_diff(time.ticks_ms(), start);
            if (w_sta.isconnected()): #{
                # Connected
                print("[BOOT  ] Connected to " + config.config['ssid']);
                print("[BOOT  ]   IP: "        + w_sta.ifconfig()[0]);
                break;
            #}
        #}

        if (delta >= timeout_net_ms): #{
            # Timeout
            print("[BOOT  ] Timeout connecting to " + config.config['ssid']);
            w_sta.active(False);
        #}
    else: #}{
        print("[BOOT  ] No SSID defined...");
        w_sta.active(False);
    #}
else : #}{
    print("[BOOT  ] No config found...");
#}

# vim:ts=4:tw=80:sw=4:et:ai:si
