from utils import exists;
import os;
import json;

config = {
     'ssid': ''
    ,'pass': ''
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

    print("[CONFIG] Saving: " + str(config));
    f = open('config.json', 'w');
    print("[CONFIG] A: " + str(json.dumps(config)));
    #f.write(json.dumps(config, indent=4));
    f.write(json.dumps(config));
    f.close();
#}

# vim:ts=4:tw=80:sw=4:et:ai:si
