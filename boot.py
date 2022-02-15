# This file is executed on every boot (including wake-boot from deepsleep)

import gc;
import time;

import globs;
import debug;

try: #{
    gc.collect();

    print("\n\n");
    print("[BOOT  ] NightyNight D1 booting...");

    import config;
    import ui;

    # LED off
    ui.led_off();

    # Disable network for now
    ui.w_sta.active(False);
    ui.w_ap.active(False);

    # Network timeout in ms
    timeout_net_ms = 30000;

    # Initialise Configuration mode by holding button down on boot
    config_mode = False;

    # Is button pressed?
    if (not ui.p_but.value()): #{
        # Pressed
        print("[BOOT  ] Button pressed. Debug mode?");

        for i in range(8, 0, -1): #{
            # Little flash
            ui.led_on();
            time.sleep(float(i) / 10.0); # i * 100 msec
            ui.led_toggle();
            time.sleep(0.1); # 100 msec

            # Not Debug, continue boot as normal
            if (ui.p_but.value()): break;
        #}

        # If still pressing, Debug mode, otherwise config mode
        if (not ui.p_but.value()): #{
            # DEBUG TIME!
            debug.debug_mode();
        else: #}{
            print("[BOOT  ] (Re)Configuration mode requested...");
            globs.mode = globs.MODE_CONFIG;
        #}
    #}

    # Normal boot (or config) here

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
                globs.mode = globs.MODE_CONFIG;
            #}
        else: #}{
            print("[BOOT  ] No SSID defined, forcing config mode...");
            globs.mode = globs.MODE_CONFIG;
        #}
    else : #}{
        print("[BOOT  ] No config found, forcing config mode...");
        globs.mode = globs.MODE_CONFIG;
    #}

    # Did they choose config (or did we fail to connect)?
    if (globs.mode == globs.MODE_CONFIG): #{
        # Configuration mode

        print("[BOOT  ] Entering (re)configuration mode...");
    #}

except KeyboardInterrupt: #}{
    print("Break");
    debug.debug_mode();
#}

# vim:ts=4:tw=80:sw=4:et:ai:si
