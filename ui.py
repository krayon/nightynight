from machine import Pin;
import time;
import network;

# Network timeout in ms
TIMEOUT_NET_MS  = const(30000);
NETWORK_CHANNEL = const(   11);

# GPIOs
p_but = Pin(12, Pin.IN , Pin.PULL_UP); # Button (D6)
p_led = Pin( 2, Pin.OUT);              # (Blue) Status LED (D4)

# Interfaces
w_sta = network.WLAN(network.STA_IF);
w_ap  = network.WLAN(network.AP_IF);

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

def net_connect(ssid='', password='', timeout=TIMEOUT_NET_MS): #{
    w_sta.active(True);
    w_sta.connect(ssid, password);

    start = time.ticks_ms();
    delta = 0;
    while (delta < timeout): #{
        time.sleep(0.7); # 700 msec
        delta = time.ticks_diff(time.ticks_ms(), start);
        if (w_sta.isconnected()): return True;
    #}

    # Timeout

    w_sta.active(False);
    return False;
#}

def net_ap_listen(pre_ssid='', password='', channel=NETWORK_CHANNEL, timeout=TIMEOUT_NET_MS): #{
    w_ap.active(True);
    time.sleep(1);
    w_ap.config(
         essid    = pre_ssid + w_ap.ifconfig()[0]
        ,channel  = channel
        ,authmode = network.AUTH_WPA2_PSK
        ,password = password
    );

    start = time.ticks_ms();
    delta = 0;
    while (delta < timeout): #{
        time.sleep(0.7); # 700 msec
        delta = time.ticks_diff(time.ticks_ms(), start);
        if (w_ap.active()): return True;
    #}

    # Timeout?!

    w_ap.active(False);
    return False;
#}

# vim:ts=4:tw=80:sw=4:et:ai:si
