import time;
import ui;

import globs;

def debug_mode(): #{
    print("[DEBUG ] Mode: Debug");

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

    globs.mode = globs.MODE_DEBUG;
    import sys;
    sys.exit(0);

    #HARD# # Soft reset? (no more, now REPL)
    #HARD# import sys;
    #HARD# sys.exit();

    # Hard reset
    import machine;
    machine.reset();
#}
