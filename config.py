from utils import exists;
import json;

config = {
     'ssid':      ''
    ,'pass':      ''
    ,'mqttserv':  ''
    ,'mqtttopic': ''
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

# vim:ts=4:tw=80:sw=4:et:ai:si
