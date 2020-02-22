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
import config;

# Interfaces
w_sta = network.WLAN(network.STA_IF);
w_ap  = network.WLAN(network.AP_IF);

# GPIOs
p_but = Pin(12, Pin.IN, Pin.PULL_UP); # Button
p_led = Pin(2, Pin.OUT); # LED

# Network timeout in ms
timeout_net_ms = 30000;
net_channel    = 11;

w_ap.active(False);

# Initialise Configuration mode by holding button down on boot
initconfig = False;
if (not p_but.value()): #{
    # Pressed
    print("[BOOT  ] (Re)Configuration mode requested...");
    initconfig = True;
#}

# LED init
v_led = 1;
p_led.value(v_led); # Turn the LED off

# Load Configuration
if (config): #{
    print("[BOOT  ] Loading configuration...");
    config.config_load();

    if (initconfig): #{
        print("[BOOT  ] Skipping wifi setup for config mode...");
    #}

    if (
        (not initconfig)
        and config.config
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
            initconfig = True;
        #}
    else: #}{
        w_sta.active(False);
        initconfig = True;
    #}
#}

# Did they initialise config (or did we fail to connect)?
if (initconfig): #{

    # Configuration mode

    from ubinascii import hexlify;

    print("[BOOT  ] Entering (re)configuration mode...");

    uid = hexlify(machine.unique_id()).decode();

    w_ap.active(True);
    time.sleep(1);
    w_ap.config(
         essid    = 'NightyNight-' + uid + '-' + w_ap.ifconfig()[0]
        ,channel  = net_channel
        ,authmode = network.AUTH_WPA2_PSK
        ,password = 'configure'    + uid
    );

    import webserver;
    webserver.webserver_start();
else: #}{

    # Normal mode

    while True: #{
        v_led = 0 if v_led == 1 else 1;
        p_led.value(v_led);
        print("[LOOP  ] LED (" + str(v_led) + ")");
        time.sleep(1); # 1 sec

        # Button breaks out of loop
        if (not p_but.value()): break;
    #}
#}

# vim:ts=4:tw=80:sw=4:et:ai:si
