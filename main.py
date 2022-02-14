# Normal mode

import gc;
import time;

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

# vim:ts=4:tw=80:sw=4:et:ai:si
