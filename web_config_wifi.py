import gc;
import globs;
import config;

from web_pyhtml import pyhtml_parser;

# We need a special manual dictionary of variables because uPython eval()
# doesn't support local variables (
# https://docs.micropython.org/en/latest/genrst/core_language.html#code-running-in-eval-function-doesn-t-have-access-to-local-variables
# )
vars_com = {
     'title': ''
    ,'ver':   ''
    ,'uid':   ''
    ,'mac':   ''
    ,'oper':  ''
    ,'style': ''
    ,'msg':   ''

    ,'ssid':  ''
};

# Returns:
#   -
def fill_vars_com(): #{
    global vars_com;

    print("web_config_wifi.fill_vars_com()");

    import os;

    # Variables
    vars_com['title'] = globs.prod + " " + globs.desc;
    vars_com['ver']   = '<a href="' + globs.url + '">' \
        + vars_com['title'] + " " + globs.ver + "<br>\n" \
        + "on " + os.uname().machine + " (" + os.uname().sysname + ") " + "<br>\n" \
        + "uPython " + os.uname().version + " (" + os.uname().release + ")" \
        + '</a>';
    vars_com['uid'] = globs.uid;
    vars_com['mac'] = globs.mac;

    if (config): #{
        config.config_load();

        if (config.config): #{
            if ('ssid' in config.config): #{
                vars_com['ssid'] = config.config['ssid'];
            #}
        #}
    #}

    gc.collect();
#}
fill_vars_com()

# Returns:
#   <s:buffer>, <i:next_offset>
def GET(size_buf, offset, vardict, body): #{
    global vars_com;

    print("web_config_wifi.GET(size_buf:%d, offset:%d, vardict, body)" % (size_buf, offset));

    buf    = '';
    read   =  0;

    if (offset == 0): #{
        vars_com['oper']  = 'GET';
        vars_com['style'] = '';
        vars_com['msg']   = '';
    #}

    tag, buf, read = pyhtml_parser('web_config_wifi.pyhtml', size_buf, offset, vardict, body);
    if (tag): #{
        print("Processing py tag:|" + buf + "|");
        buf = eval(buf, vars_com);
    #}

    return buf, read;
#}

# Returns:
#   <s:buffer>, <i:next_offset>
def POST(size_buf, offset, vardict, body): #{
    global vars_com;

    print("web_config_wifi.POST(size_buf:%d, offset:%d, vardict, body)" % (size_buf, offset));

    buf    = '';
    read   =  0;

    if (offset == 0): #{
        vars_com['oper']  = 'POST';
        vars_com['style'] = '';
        vars_com['msg']   = '';
    #}

    bodyvararr = body.split('&');
    bodyvardict = dict(map(lambda s : map(str.strip, s.split('=', 1)), bodyvararr));

    if (bodyvardict): #{
        for key, val in bodyvardict.items(): #{
            if (not key): continue;

            if (key == 'ssid'): #{
                if (config and config.config): #{
                    vars_com['ssid'] = val;
                    config.config['ssid'] = vars_com['ssid'];
                #}

            elif (key == 'passphrase'): #}{
                if (config and config.config): #{
                    config.config['pass'] = val;
                #}
            #}
        #}
    #}

    if (offset == 0): #{
        try: #{
            config.config_save();

            # Saved

            vars_com['style'] = 'confirmed';
            vars_com['msg']   = 'Saved';

        except: #}{
            vars_com['style'] = 'warning';
            vars_com['msg']   = 'Error saving config!';
        #}
    #}

    tag, buf, read = pyhtml_parser('web_config_wifi.pyhtml', size_buf, offset, vardict, body);
    if (tag): #{
        print("Processing py tag:|" + buf + "|");
        buf = eval(buf, vars_com);
    #}

    return buf, read;
#}

# vim:ts=4:tw=80:sw=4:et:ai:si
