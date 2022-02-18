import gc;
import json;

from utils import exists;

config = {
     'ssid':        ''
    ,'pass':        ''
    ,'timeout_net': 30000
    ,'mqttserv':    ''
    ,'mqtttopic':   ''
    ,'mqttport':     1880
};

def config_load(): #{
    global config;

    print("[CONFIG] Loading...");

    if (exists('config.json')): #{
        f = open('config.json', 'r');
        config = json.load(f);
        print("[CONFIG] " + str(config));
    #}
#}

def config_save(): #{
    global config;

    print("[CONFIG] Saving config");
    f = open('config.json', 'w');
    print("[CONFIG] JSON: " + str(json.dumps(config)));
    f.write(str(json.dumps(config)));
    f.close();
#}

def launch_app(): #{
    print("\n\n");
    print("[CONFIG] Config App");

    gc.collect();

    import web_server;
    web_server.start();
#}

# vim:ts=4:tw=80:sw=4:et:ai:si
