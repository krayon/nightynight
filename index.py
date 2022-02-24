import os;
import globs;

# Returns:
#   <s:buffer>, <i:next_offset>
def index(size_buf, offset, vardict, body): #{
    print("index.index(size_buf:%d, offset:%d, vardict, body)" % (size_buf, offset));
    return "", -1;
#}

# Returns:
#   <s:buffer>
def __DEFAULT_PAGE(title, ver, uid, mac): #{
    return """<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"><html><head><meta content="text/html; charset=ISO-8859-1" http-equiv="content-type"><title>""" + title + """</title><link rel="stylesheet" type="text/css" href="web_nn.css"></head><body><div class="mainTables"><table class="mainTables"><tr><td rowspan="6">&nbsp;</td><td colspan="2">""" + title + """</td><td rowspan="6">&nbsp;</td></tr><tr><td>Device Unique ID:</td><td class="ro"><pre>""" + uid + """</pre></td></tr><tr><td>MAC Address:</td><td class="ro"><pre>""" + mac + """</pre></td></tr><tr><td colspan=2>&nbsp;</td></tr><tr><td colspan=2><a href="web_reboot.py" >Reboot</a></td></tr><tr><td colspan=2>&nbsp;</td></tr><tr><td class="byline ro" colspan=4><em>""" + ver + """</em></td></tr></table></div></body></html>""";
#}

# Returns:
#   <s:buffer>, <i:next_offset>
def GET(size_buf, offset, vardict, body): #{
    print("index.GET(size_buf:%d, offset:%d, vardict, body)" % (size_buf, offset));

    title = globs.prod + " " + globs.desc;
    ver = '<a href="' + globs.url + '">' \
        + title + " " + globs.ver + "<br>\n" \
        + "on " + os.uname().machine + " (" + os.uname().sysname + ") " + "<br>\n" \
        + "uPython " + os.uname().version + " (" + os.uname().release + ")" \
        + '</a>';

    return "HTTP/1.0 200 OK\n" + "Content-Type: text/html\n\n" + __DEFAULT_PAGE(title, ver, globs.uid, globs.mac), -1;
#}

### # Returns:
### #   <s:buffer>, <i:next_offset>
### def endGET(size_buf, offset, vardict, body): #{
###     print("index.endGET()");
###
###     return "HTTP/1.0 200 OK\nContent-Type: text/html\n\n", -1;
### #}

# vim:ts=4:tw=80:sw=4:et:ai:si
