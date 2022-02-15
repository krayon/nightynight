# Normal mode

import gc;
import time;

import globs;
import debug;

if (not globs.mode == globs.MODE_APP): #{
    import sys;
    sys.exit(0);
#}

try: #{
    gc.collect();

    print("\n\n");
    print("[APP   ] Normal boot");

    import ui;

    ui.led_off();
    last_but = 1;
    while True: #{
        # Button turns LED on and off

        if (not ui.p_but.value() == last_but): #{
            ui.led_toggle();
            last_but = ui.p_but.value();

            print(
                "[APP   ] LED: %d, BUT: %d"
                % (ui.v_led, last_but)
            );
        #}

        time.sleep(0.1); # 100 ms
    #}

except KeyboardInterrupt: #}{
    print("Break");
    debug.debug_mode();
#}

# vim:ts=4:tw=80:sw=4:et:ai:si
