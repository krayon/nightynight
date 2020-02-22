import config;

def web_config_wifi(): #{
    print("web_config_wifi.web_config_wifi()");
    return "Namespace function!";
#}

def __DEFAULT_PAGE(ssid, mqttserv, mqtttopic): #{
    ret="""<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
  <head>
    <meta content="text/html; charset=ISO-8859-1" http-equiv="content-type">
    <title>Nighty Nighty (D1 uPython Edition)</title>
    <link rel="stylesheet" type="text/css" href="web_nn.css">
  </head>
  <body>
    <div class="mainTables">
      <form method="POST">
        <table class="mainTables">
          <tr>
            <td rowspan="8">&nbsp;</td>
            <td colspan="2">Nighty Nighty (D1 uPython Edition)</td>
            <td rowspan="8">&nbsp;</td>
          </tr>
  
          <tr>
            <td>SSID:</td>
            <td><input
              name="ssid"
              type="text"
              value=""" + '"' + ssid + '"' + """
              placeholder="My Network SSID"
            ></td>
          </tr>
          <tr>
            <td>Passphrase:</td>
            <td><input
              name="passphrase"
              type="password"
              value=""
              placeholder="My Network Passphrase"
            ></td>
          </tr>

          <tr>
            <td colspan=2>&nbsp;</td>
          </tr>

          <tr>
            <td>MQTT Server:</td>
            <td><input
              name="mqttserv"
              type="text"
              value=""" + '"' + mqttserv + '"' + """
              placeholder="My MQTT Server Address"
            ></td>
          </tr>
          <tr>
            <td>MQTT Topic:</td>
            <td><input
              name="mqtttopic"
              type="text"
              value=""" + '"' + mqtttopic + '"' + """
              placeholder="My MQTT Topic"
            ></td>
          </tr>

          <tr>
            <td colspan=2>&nbsp;</td>
          </tr>

          <tr>
            <td colspan=2><input
              type="submit"
              value="Save"
            ></td>
          </tr>
        </table>
      </form>
    </div>
  </body>
</html>""";

    return ret;
#}

def GET(vardict): #{
    print("web_config_wifi.GET()");

    ssid="";
    mqttserv="";
    mqtttopic="";
    if (config): #{
        config.config_load();

        if (config.config): #{
            if ('ssid' in config.config): #{
                ssid=config.config['ssid'];
            #}

            if ('mqttserv' in config.config): #{
                mqttserv=config.config['mqttserv'];
            #}

            if ('mqtttopic' in config.config): #{
                mqtttopic=config.config['mqtttopic'];
            #}
        #}
    #}

    ret = """HTTP/1.0 200 OK
Content-Type: text/html

""" + __DEFAULT_PAGE(ssid, mqttserv, mqtttopic);

    return ret.replace('\n', '\r\n');
#}

def POST(vardict): #{
    print("web_config_wifi.POST()");

    ret = "";
    ssid = "";
    mqttserv = "";
    mqtttopic = "";

    if (vardict): #{
        for key in vardict: #{
            if (key): #{
                if (key == 'ssid'): #{
                    if (config and config.config): #{
                        ssid = vardict[key];
                        config.config['ssid'] = ssid;
                    #}

                elif (key == 'passphrase'): #{
                    if (config and config.config): #{
                        config.config['pass'] = vardict[key];
                    #}
                #}

                elif (key == 'mqttserv'): #{
                    if (config and config.config): #{
                        mqttserv = vardict[key];
                        config.config['mqttserv'] = vardict[key];
                    #}
                #}

                elif (key == 'mqtttopic'): #{
                    if (config and config.config): #{
                        mqtttopic = vardict[key];
                        config.config['mqtttopic'] = vardict[key];
                    #}
                #}

                ret = ret + key + ": " + vardict[key] + "\n"
            #}
        #}
    #}

    try: #{
        config.config_save();

        # Saved
        ret="""HTTP/1.0 302 Found
Location: /
Content-Type: text/html

<html>
<head>
<title>Config Saved</title>
<meta http-equiv="Refresh" content="3; url=/" />
</head>
<body>
<h1>Config Saved</h1>
</body>
</html>
"""

        return ret.replace('\n', '\r\n');
    except: #}{
        return "HTTP/1.0 200 OK\r\n" + "Content-Type: text/html\r\n" + "\r\n" + __DEFAULT_PAGE(ssid, mqttserv, mqtttopic).replace('\n', '\r\n');
    #}

    #return "Content-Type: text/html\r\n\r\n" + "POST: " + ret + ", " + default;
    #return "HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n" + "POST: " + ret;
#}

# vim:ts=4:tw=80:sw=4:et:ai:si
