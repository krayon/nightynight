# HTTP server based on the uasyncio example script by J.G. Wezensky

import gc;
import uasyncio as asyncio;
from utils import exists;

#webroot = 'wwwroot';
webroot = '';
default = 'index.html';

# Looks up the content-type based on the file extension
def get_mime_type(file): #{
    print("get_mime_type(" + str(file) + ")");

    if file.endswith(".html"):    return "text/html"      , False;
    if file.endswith(".css" ):    return "text/css"       , True;
    if file.endswith(".js"  ):    return "text/javascript", True;
    if file.endswith(".png" ):    return "image/png"      , True;
    if file.endswith(".gif" ):    return "image/gif"      , True;
    if file.endswith(".jpeg") or file.endswith(".jpg"):
                                  return "image/jpeg"     , True;
    return "text/plain", False;
#}

# Breaks an HTTP request into its parts and boils it down to a physical file
# (if possible)
def decode_path(req): #{
    global webroot, default;

    cmd, headers = req.decode("utf-8").split('\r\n', 1)
    parts = cmd.split(' ')
    method, path = parts[0], parts[1]
    # remove any query string
    query = ''
    r = path.find('?')
    if r > 0:
        query = path[r:]
        path = path[:r]
    # check for use of default document
    if path == '/':
        path = default
    else:
        path = path[1:]
    # return the physical path of the response file
    return webroot + '/' + path
#}

@asyncio.coroutine
def serve(reader, writer):
    try:
        file = decode_path((yield from reader.read()))
        if exists(file):
            mime_type, cacheable = get_mime_type(file)
            yield from writer.awrite("HTTP/1.0 200 OK\r\n")
            yield from writer.awrite("Content-Type: {}\r\n".format(mime_type))
            if cacheable:
                yield from writer.awrite("Cache-Control: max-age=86400\r\n")
            yield from writer.awrite("\r\n")

            f = open(file, "rb")
            buffer = f.read(512)
            while buffer != b'':
                yield from writer.awrite(buffer)
                buffer = f.read(512)
            f.close()
        else:
            yield from writer.awrite("HTTP/1.0 404 NA\r\n\r\n")
    except:
        raise
    finally:
        yield from writer.aclose()

@asyncio.coroutine
def MY_serve(reader, writer): #{
    print("serve()");
    data = '';
    while 1: #{
        print("while 1");
        more = (yield from reader.read());
        more = more.decode() if more is not None else '';
        print(more);
        if (len(more) < 1): #{
            print("NO MORE DATA");
            break;
        #}

        print("more: " + more);
        data += more;
    #}
    print(data)

    try:
        file = decode_path((yield from reader.read()))
        print("Serving file: " + file);
        if exists(file): #{
            mime_type, cacheable = get_mime_type(file)
            if file.endswith(".py"): #{
                mod = None;
                method = 'POST'; # FIXME: REMOVE THIS TEMP

                vardict = {}; # FIXME: REMOVE THIS TEMP
                if (not vardict): #{
                    vardict = {};
                #}

                try: #{
                    modpath = file.rsplit(".", 1)[0];
                    modname = modpath.rsplit("/", 1)[1];
                    mod     = __import__(modpath);
                    print("modpath: " + modpath);
                    print("modname: " + modname);

                except: #}{
                    yield from writer.awrite("HTTP/1.0 500 Exec1\r\n\r\n");
                    yield from writer.aclose();
                    return;
                #}

                try: #{
                    #modfunc = getattr(mod, modname);
                    modfunc = getattr(mod, method);

                except: #}{
                    yield from writer.awrite("HTTP/1.0 500 Exec2\r\n\r\n");
                    yield from writer.aclose();
                    return;
                #}

                #try: #{
                #    # "Execute" the python module (or more specifically, it's
                #    # function of the same name) ... UPDATE: Now use a function
                #    # named the method (eg. GET, POST etc)
                #    #
                #    # NOTE: You MUST output Content-Type and newline yourself
                #    buffer = modfunc(vardict);

                #    yield from writer.awrite("HTTP/1.0 200 OK\r\n");
                #    #yield from writer.awrite("Content-Type: {}\r\n".format(mime_type));
                #    #yield from writer.awrite("\r\n");
                #    yield from writer.awrite(buffer);

                #except: #}{
                #    yield from writer.awrite("HTTP/1.0 500 Exec3\r\n\r\n");
                #    yield from writer.aclose();
                #    return;
                ##}

                buffer = modfunc(vardict);
                ####yield from writer.awrite("HTTP/1.0 200 OK\r\n");

                ##### FIXME: if buffer comes back as nothing (such as if I
                ##### async.sleep in the func) then write.awrite fails as buffer
                ##### is of type 'generator' and doesn't have .len()

                ###yield from writer.awrite(buffer);
                ##if (buffer): yield from writer.awrite(buffer);
                #if (buffer is not None): yield from writer.awrite(buffer);
                yield from writer.awrite(buffer);

                try: #{
                    modfunc = getattr(mod, 'end' + method);

                except: #}{
                    yield from writer.aclose();
                    return;
                #}

                buffer = modfunc(vardict);

                ##### FIXME: if buffer comes back as nothing (such as if I
                ##### async.sleep in the func) then write.awrite fails as buffer
                ##### is of type 'generator' and doesn't have .len()

                yield from writer.awrite(buffer);

            else: #}{
                # Headers
                yield from writer.awrite("HTTP/1.0 200 OK\r\n");
                yield from writer.awrite("Content-Type: {}\r\n".format(mime_type));
                if cacheable: #{
                    yield from writer.awrite("Cache-Control: max-age=86400\r\n");
                #}
                yield from writer.awrite("\r\n");

                f = open(file, "rb");
                buffer = f.read(size_buffer);
                while buffer != b'': #{
                    yield from writer.awrite(buffer);
                    buffer = f.read(size_buffer);
                #}
                f.close();
            #}
        else: #}{
            yield from writer.awrite("HTTP/1.0 404 NA\r\n\r\n")
        #}
    except:
        raise
    finally:
        yield from writer.aclose()
#}

def start(): #{
    import logging;
    logging.basicConfig(level=logging.ERROR);

    print("Initialising event loop...");
    loop = asyncio.get_event_loop();
    print("Starting server...");
    loop.call_soon(asyncio.start_server(serve, "0.0.0.0", 80, 20));
    print("Entering loop...");
    loop.run_forever();
    loop.close();
#}

# vim:ts=4:tw=80:sw=4:et:ai:si
