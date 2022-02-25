import os;
import globs;

from web_pyhtml import pyhtml_parser;

# Returns:
#   <s:buffer>, <i:next_offset>
def GET(size_buf, offset, vardict, body): #{
    print("web_reboot.GET(size_buf:%d, offset:%d, vardict, body)" % (size_buf, offset));

    buf    = '';
    read   =  0;

    # Variables
    title = globs.prod + " " + globs.desc;
    ver = '<a href="' + globs.url + '">' \
        + title + " " + globs.ver + "<br>\n" \
        + "on " + os.uname().machine + " (" + os.uname().sysname + ") " + "<br>\n" \
        + "uPython " + os.uname().version + " (" + os.uname().release + ")" \
        + '</a>';
    uid = globs.uid;
    mac = globs.mac;

    tag, buf, read = pyhtml_parser('web_reboot.pyhtml', size_buf, offset, vardict, body);
    if (tag): #{
        print("Processing py tag:|" + buf + "|");
        buf = eval(buf, {
             'title': title
            ,'ver':   ver
            ,'uid':   uid
            ,'mac':   mac
        });
    #}

    return buf, read;
#}

# Returns:
#   <s:buffer>, <i:next_offset>
def endGET(size_buf, offset, vardict, body): #{
    print("web_reboot.endGET(size_buf:%d, offset:%d, vardict, body)" % (size_buf, offset));

    import machine;
    import time;

    time.sleep(5);

    machine.reset();

    return '', -1;
#}

# vim:ts=4:tw=80:sw=4:et:ai:si
