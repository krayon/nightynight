# Main entry point

import gc;
import time;

import globs;
import debug;

try: #{
    gc.collect();

    print("\n\n");
    print("[MAIN  ] Main entry point");

    if (globs.mode == globs.MODE_CONFIG): #{
        print("[MAIN  ] Mode: Config");
        import config;
        config.launch_app();

        time.sleep(2); # 2 secs

        # Hard reset
        import machine;
        machine.reset();

    elif (globs.mode == globs.MODE_APP): #{
        print("[MAIN  ] Mode: App");
        import app;
        app.main();

        time.sleep(2); # 2 secs

        # Hard reset
        import machine;
        machine.reset();

    elif (globs.mode == globs.MODE_DEBUG): #{
        print("[MAIN  ] Mode: Debug");

        # Fall through after debug exits - Once we exit, REPL will happen
    #}

except KeyboardInterrupt: #}{
    print("Break");
    debug.debug_mode();
#}

# vim:ts=4:tw=80:sw=4:et:ai:si
