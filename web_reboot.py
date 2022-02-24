import os;
import globs;

# Returns:
#   <s:buffer>, <i:next_offset>
def web_reboot(size_buf, offset, vardict, body): #{
    print("web_reboot.web_reboot(size_buf:%d, offset:%d, vardict, body)" % (size_buf, offset));
    return "", -1;
#}

def __DEFAULT_PAGE(title): #{
    return """<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"><html><head><meta content="text/html; charset=ISO-8859-1" http-equiv="content-type"><title>""" + title + """</title><link rel="stylesheet" type="text/css" href="web_nn.css"></head><body><h1>Rebooting in 5 seconds...</h1></body></html>""";
#}

# Returns:
#   <s:buffer>, <i:next_offset>
def GET(size_buf, offset, vardict, body): #{
    print("web_reboot.GET(size_buf:%d, offset:%d, vardict, body)" % (size_buf, offset));

    title = globs.prod + " " + globs.desc;

    return "HTTP/1.0 200 OK\nContent-Type: text/html\n\n" + __DEFAULT_PAGE(title), -1;
#}

# Returns:
#   <s:buffer>, <i:next_offset>
def endGET(size_buf, offset, vardict, body): #{
    print("web_reboot.endGET(size_buf:%d, offset:%d, vardict, body)" % (size_buf, offset));

    import machine;
    import time;

    time.sleep(5);

    machine.reset();

    return "HTTP/1.0 200 OK\nContent-Type: text/html\n\n", -1;
#}

# vim:ts=4:tw=80:sw=4:et:ai:si
