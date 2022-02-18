import os;
import globs;

def index(vardict, body, page=0): #{
    print("index.index()");
    return "", False;
#}

def __DEFAULT_PAGE(title, ver, uid, mac): #{
    return """<<<<<MINIFIED_CONTENT>>>>>""";
#}

def GET(vardict, body, page=0): #{
    print("index.GET()");

    title = globs.prod + " " + globs.desc;
    ver = '<a href="' + globs.url + '">' \
        + title + " " + globs.ver + "<br>\n" \
        + "on " + os.uname().machine + " (" + os.uname().sysname + ") " + "<br>\n" \
        + "uPython " + os.uname().version + " (" + os.uname().release + ")" \
        + '</a>';

    return """HTTP/1.0 200 OK
Content-Type: text/html

""" + __DEFAULT_PAGE(title, ver, globs.uid, globs.mac), False;

#}

# vim:ts=4:tw=80:sw=4:et:ai:si
