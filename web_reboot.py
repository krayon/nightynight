import machine;
import time;

def web_reboot(): #{
    print("web_reboot.web_reboot()");
    return "Namespace function!";
#}

def __DEFAULT_PAGE(): #{
    ret="""<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
  <head>
    <meta content="text/html; charset=ISO-8859-1" http-equiv="content-type">
    <title>Nighty Nighty (D1 uPython Edition)</title>
  </head>
  <body>
    <h1>Rebooting in 5 seconds...</h1>
  </body>
</html>""";

    return ret;
#}

def GET(vardict): #{
    print("web_reboot.GET()");

    ret = """HTTP/1.0 200 OK
Content-Type: text/html

""" + __DEFAULT_PAGE();

    return ret.replace('\n', '\r\n');
#}

def endGET(vardict): #{
    print("web_reboot.endGET()");

    time.sleep(5);

    ret = """HTTP/1.0 200 OK
Content-Type: text/html

""";

    machine.reset();
    return ret.replace('\n', '\r\n');
#}
