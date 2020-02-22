# Normal mode

while True: #{
    v_led = 0 if v_led == 1 else 1;
    p_led.value(v_led);
    print("[LOOP  ] LED (" + str(v_led) + ")");
    time.sleep(1); # 1 sec

    # Button breaks out of loop
    if (not p_but.value()): break;
#}

# vim:ts=4:tw=80:sw=4:et:ai:si
