from machine import Pin;
import time;
import network;

def led_toggle(): #{
    global v_led, p_led;
    v_led = 0 if v_led == 1 else 1;
    p_led.value(v_led);
#}

def led_on(): #{
    global v_led;
    v_led = 1; # Off
    led_toggle();
#}

def led_off(): #{
    global v_led;
    v_led = 0; # On
    led_toggle();
#}

def led_flash(n=1): #{
    for c in range(n): #{
        led_toggle();
        time.sleep(0.25); # 250 ms
        led_toggle();
        time.sleep(0.25); # 250 ms
    #}
#}

# GPIOs
p_but = Pin(12, Pin.IN , Pin.PULL_UP); # Button (D6)
p_led = Pin( 2, Pin.OUT);              # (Blue) Status LED (D4)

# Interfaces
w_sta = network.WLAN(network.STA_IF);
w_ap  = network.WLAN(network.AP_IF);

# vim:ts=4:tw=80:sw=4:et:ai:si
