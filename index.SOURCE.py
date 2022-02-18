import os;
import globs;
import config;

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
    ver = title + " " + globs.ver + "<br>\non " + os.uname().machine + " (" + os.uname().sysname + ") " + "<br>\nuPython " + os.uname().version + " (" + os.uname().release + ")";

    return """HTTP/1.0 200 OK
Content-Type: text/html

""" + __DEFAULT_PAGE(title, ver, globs.uid, globs.mac), False;

#}

# vim:ts=4:tw=80:sw=4:et:ai:si
