import os;
import globs;

def web_reboot(vardict, body, page=0): #{
    print("web_reboot.web_reboot()");
    return "", False;
#}

def __DEFAULT_PAGE(title): #{
    return """<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"><html><head><meta content="text/html; charset=ISO-8859-1" http-equiv="content-type"><title>""" + title + """</title><link rel="stylesheet" type="text/css" href="web_nn.css"></head><body><h1>Rebooting in 5 seconds...</h1></body></html>""";
#}

def GET(vardict, body, page=0): #{
    print("web_reboot.GET()");

    title = globs.prod + " " + globs.desc;

    return """HTTP/1.0 200 OK
Content-Type: text/html

""" + __DEFAULT_PAGE(title), False;

#}

def endGET(vardict, body, page=0): #{
    print("web_reboot.endGET()");

    import machine;
    import time;

    time.sleep(5);

    machine.reset();

    return """HTTP/1.0 200 OK
Content-Type: text/html

""", False;

#}

# vim:ts=4:tw=80:sw=4:et:ai:si
