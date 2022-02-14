from machine import Pin;
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

# GPIOs
p_but = Pin(12, Pin.IN , Pin.PULL_UP); # Button (D6)
p_led = Pin( 2, Pin.OUT);              # (Blue) Status LED (D4)

# LED init - turn it off
led_off();

# Interfaces
w_sta = network.WLAN(network.STA_IF);
w_ap  = network.WLAN(network.AP_IF);

# vim:ts=4:tw=80:sw=4:et:ai:si
