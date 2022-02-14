# Normal mode

import gc;
import time;

import globs;
import debug;

if (not globs.run): #{
    import sys;
    sys.exit(0);
#}

try: #{
    gc.collect();

    print("\n\n");
    print("[MAIN  ] Normal boot");

    import ui;

    while True: #{
        ui.led_toggle();
        print("[LOOP  ] LED (" + str(ui.v_led) + ")");
        time.sleep(1); # 1 sec

        # Button breaks out of loop
        if (not ui.p_but.value()): break;
    #}

except KeyboardInterrupt: #}{
    print("Break");
    debug.debug_mode();
#}

# vim:ts=4:tw=80:sw=4:et:ai:si
