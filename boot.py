# This file is executed on every boot (including wake-boot from deepsleep)

import gc;
import time;

import debug;

try: #{
    gc.collect();

    print("\n\n");
    print("[BOOT  ] NightyNight D1 booting...");

    import config;
    import ui;

    # Disable network for now
    ui.w_sta.active(False);
    ui.w_ap.active(False);

    # Network timeout in ms
    timeout_net_ms = 30000;

    # Is button pressed?
    if (not ui.p_but.value()): #{
        # Pressed
        print("[BOOT  ] Button pressed. Debug mode?");

        for i in range(1, 10): #{
            # Little flash
            ui.led_toggle();
            time.sleep(float(i) / 10.0); # i * 100 msec

            # Not Debug, continue boot as normal
            if (ui.p_but.value()): break;
        #}

        # If still pressing, Debug mode
        if (not ui.p_but.value()): #{
            # DEBUG TIME!
            debug.debug_mode();
        #}
    #}

    # Normal boot here

    # Turn the LED off
    ui.led_off();

    # Load Configuration
    if (config): #{
        print("[BOOT  ] Loading configuration...");
        config.config_load();

        if (
            config.config
            and 'ssid' in config.config
            and len(config.config['ssid']) > 0
            and 'pass' in config.config
            and len(config.config['pass']) > 0
        ): #{
            print("[BOOT  ] Existing AP ("
            + config.config['ssid']
            + ") configured, connecting...");

            ui.w_sta.active(True);
            ui.w_sta.connect(config.config['ssid'], config.config['pass']);

            start = time.ticks_ms();
            delta = 0;
            while (delta < timeout_net_ms): #{



                # Little flash
                ui.led_toggle();
                time.sleep(0.1); # 100 msec
                ui.led_toggle();
                time.sleep(0.1); # 100 msec
                ui.led_toggle();
                time.sleep(0.1); # 100 msec



                time.sleep(0.7); # 700 msec
                delta = time.ticks_diff(time.ticks_ms(), start);
                if (ui.w_sta.isconnected()): #{
                    # Connected
                    print("[BOOT  ] Connected to " + config.config['ssid']);
                    print("[BOOT  ]   IP: "        + ui.w_sta.ifconfig()[0]);
                    break;
                #}
            #}

            if (delta >= timeout_net_ms): #{
                # Timeout
                print("[BOOT  ] Timeout connecting to " + config.config['ssid']);
                ui.w_sta.active(False);
            #}
        else: #}{
            print("[BOOT  ] No SSID defined...");
            ui.w_sta.active(False);
        #}
    else : #}{
        print("[BOOT  ] No config found...");
    #}

except KeyboardInterrupt: #}{
    print("Break");
    debug.debug_mode();
#}

# vim:ts=4:tw=80:sw=4:et:ai:si
