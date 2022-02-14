import time;
import ui;

def debug_mode(): #{
    print("[BOOT  ] Debug MODE: Confirmed");

    # Little flash
    ui.led_toggle();
    time.sleep(0.1); # 100 msec
    ui.led_toggle();
    time.sleep(0.1); # 100 msec
    ui.led_toggle();
    time.sleep(0.1); # 100 msec

    ui.led_on();
    while True: #{
        time.sleep(0.5); # 500 msec
    #}

    #HARD# # Soft reset
    #HARD# import sys;
    #HARD# sys.exit();

    # Hard reset
    import machine;
    machine.reset();
#}
