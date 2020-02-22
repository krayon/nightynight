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

# Interfaces
w_sta = network.WLAN(network.STA_IF);
w_ap  = network.WLAN(network.AP_IF);

w_ap.active(False);

p_led = Pin(2, Pin.OUT);
v_led = 1;
p_led.value(v_led); # Turn the LED off

while True: #{
    v_led = 0 if v_led == 1 else 1;
    p_led.value(v_led);
    print("[LOOP  ] LED (" + str(v_led) + ")");
    time.sleep(1); # 1 sec
#}

# vim:ts=4:tw=80:sw=4:et:ai:si
