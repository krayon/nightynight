# This file is executed on every boot (including wake-boot from deepsleep)

import gc;
import time;

import globs;
import debug;

try: #{
    gc.collect();

    print("\n\n");
    print("[BOOT  ] NightyNight D1 booting...");

    from ubinascii import hexlify;
    import machine;
    import network;

    globs.uid = hexlify(machine.unique_id()).decode();
    globs.mac = hexlify(network.WLAN().config('mac'),':').decode();

    gc.collect();

    import config;
    import ui;

    # LED off
    ui.led_off();

    # Disable network for now
    ui.w_sta.active(False);
    ui.w_ap.active(False);

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

            if (not ui.net_connect(
                 ssid     = config.config['ssid']
                ,password = config.config['pass']
                ,timeout  = config.config['timeout_net']
            )): #{
                # Timeout

                print("[BOOT  ] Timeout connecting to " + config.config['ssid']);

                ui.led_flash(1);

                globs.mode = globs.MODE_CONFIG;

            else: #}{
                # Connected

                print("[BOOT  ] Connected to " + config.config['ssid']);
                print("[BOOT  ]   IP:      "   + ui.w_sta.ifconfig()[0]);
                print("[BOOT  ]   Subnet:  "   + ui.w_sta.ifconfig()[1]);
                print("[BOOT  ]   Gateway: "   + ui.w_sta.ifconfig()[2]);
                print("[BOOT  ]   DNS:     "   + ui.w_sta.ifconfig()[3]);

                # If we are going to config mode, give the option to go with own
                # AP instead
                if (globs.mode == globs.MODE_CONFIG): #{
                    print("[BOOT  ] Waiting for explicit AP request...");
                    for i in range(8, 0, -1): #{
                        # Little flash
                        ui.led_on();
                        for j in range(i * 2): #{
                            if (not ui.p_but.value()): break;
                            time.sleep(0.050); # (i * 2) * 50 msec
                        #}
                        ui.led_toggle();

                        # Requesting own AP, disable current client connection
                        if (not ui.p_but.value()): #{
                            ui.led_on();
                            print("[BOOT  ] Own AP requested, disconnecting");
                            ui.w_sta.disconnect();
                            ui.w_sta.active(False);
                            time.sleep(1); # 1 sec
                            ui.led_toggle();
                            break;
                        #}

                        time.sleep(0.1); # 100 msec
                    #}
                #}
            #}
        else: #}{
            # No SSID set
            print("[BOOT  ] No SSID defined, forcing config mode...");

            ui.led_flash(2);
            globs.mode = globs.MODE_CONFIG;
        #}
    else : #}{
        # No config found
        print("[BOOT  ] No config found, forcing config mode...");

        ui.led_flash(3);

        globs.mode = globs.MODE_CONFIG;
    #}

    # Did they choose config (or did we fail to connect)?
    if (globs.mode == globs.MODE_CONFIG): #{
        # Configuration mode

        print("[BOOT  ] Entering (re)configuration mode...");

        # If we're connected, we are going into config mode on the AP we're
        # connected to, so no need to create our own, otherwise create one.
        if (not ui.w_sta.isconnected()): #{
            if (not ui.net_ap_listen(
                 pre_ssid = 'NightyNight-' + globs.uid + '-'
                ,password = 'configure'    + globs.uid
                ,timeout  = config.config['timeout_net']
            )): #{
                # Timeout?!

                print("[BOOT  ] Timeout initialising AP!");

                debug.sos(1);

            else: #}{
                # Listening

                print("[BOOT  ] Listening:");
                print("[BOOT  ]   ESSID:   "   + ui.w_ap.config('essid'));
                print("[BOOT  ]   Channel: "   + str(ui.w_ap.config('channel')));
                print("[BOOT  ]   IP:      "   + ui.w_ap.ifconfig()[0]);
                print("[BOOT  ]   Subnet:  "   + ui.w_ap.ifconfig()[1]);
                print("[BOOT  ]   Gateway: "   + ui.w_ap.ifconfig()[2]);
                print("[BOOT  ]   DNS:     "   + ui.w_ap.ifconfig()[3]);
            #}
        #}
    #}

except KeyboardInterrupt: #}{
    print("Break");
    debug.debug_mode();
#}

# vim:ts=4:tw=80:sw=4:et:ai:si
