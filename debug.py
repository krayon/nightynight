import time;
import ui;

import globs;

def debug_mode(): #{
    print("[BOOT  ] Debug MODE: Confirmed");

    # Little flash
    ui.led_toggle();
    time.sleep(0.05); # 50 msec
    ui.led_toggle();
    time.sleep(0.05); # 50 msec
    ui.led_toggle();
    time.sleep(0.05); # 50 msec

    # Turn the LED ON
    ui.led_on();

    # Fire up REPL

    #uart = machine.UART(0, 115200);
    #os.dupterm(uart)

    globs.run = False;
    import sys;
    sys.exit(0);

    #HARD# # Soft reset
    #HARD# import sys;
    #HARD# sys.exit();

    # Hard reset
    import machine;
    machine.reset();
#}
