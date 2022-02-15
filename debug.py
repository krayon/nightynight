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

# SOS (... --- ...)
def sos(err_code=0): #{
    try: #{
        ui.led_off();

        for i in range(10): #{
            # S (...)
            for c in range(3): #{
                ui.led_toggle();
                time.sleep(0.10);
                ui.led_toggle();
                time.sleep(0.40);
            #}

            time.sleep(0.50);

            # O (---)
            for c in range(3): #{
                ui.led_toggle();
                time.sleep(0.40);
                ui.led_toggle();
                time.sleep(0.10);
            #}

            time.sleep(0.50);

            # S (...)
            for c in range(3): #{
                ui.led_toggle();
                time.sleep(0.10);
                ui.led_toggle();
                time.sleep(0.40);
            #}

            time.sleep(2);

            # Err code
            for c in range(err_code): #{
                ui.led_toggle();
                time.sleep(0.25);
                ui.led_toggle();
                time.sleep(0.25);
            #}

            time.sleep(2);
        #}

        # Hard reset
        import machine;
        machine.reset();

    except KeyboardInterrupt: #}{
        print("Break");
        debug_mode();
    #}
#}
