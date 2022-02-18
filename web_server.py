# HTTP server based on the uasyncio example script by J.G. Wezensky

import gc;
import uasyncio as asyncio;
from utils import exists;

#webroot = 'wwwroot';
webroot = '';
default = 'index.html';

size_buffer          =  512;
size_max_http_header =  512; # TODO
size_max_http_total  = 1024;

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

# Breaks an HTTP uri request into its parts and boils it down to a physical file
# (if possible)
def decode_path(uri): #{
    global webroot, default;

    if (len(uri) == 0): return;

    print("decode_path(" + str(uri) + ")");

    try: #{
        path, varstr = uri.split('?', 1);
        vararray = varstr.split('&');
        varstr = None;
    except: #}{
        path = uri;
        vararray = [];
    #}

    print("uri:", uri, "\npath:", path, "\nvararray:", vararray);
    # uri:       '/web_config_wifi.longname.html?param1=stuff1&param2=stuff2'
    # path:      '/web_config_wifi.longname.html'
    # vararray:  ['param1=stuff1', 'param2=stuff2']

    # dict-ify the vararray pair array
    # (exception for this will be caught in caller)
    vardict = dict(map(lambda s : map(str.strip, s.split('=', 1)), vararray));

    print("vardict:", vardict);
    # vardict:   {'param1': 'stuff1', 'param2': 'stuff2'}

    # Check for use of default document
    if path == '/': #{
        path = default;
    else: #}{
        path = path[1:];
    #}

    # Return the physical path of the response file
    return webroot + '/' + path, vardict;
#}

# Larger requests would not all be delivered so we need to do multiple calls to
# piece it all together
@asyncio.coroutine
def read_complete_req(reader, writer): #{
    print("read_complete_req()");
    req = {};
    body = '';
    headers = {};
    clen = 0;
    print("1");

    # Read in complete request
    while 1: #{
        print("2");
        more = '';

        # TODO: Add timer here to trigger timeout

        # TODO: Confirm this works as I expect - read won't block first try as
        # something's waiting - that's what triggered the function call in the
        # first place?
        print("3");
        more = (yield from reader.read());
        more = more.decode() if more is not None else '';

        print("\n\n\nMORE:\n", more, "\n\n\n");

        if (len(more) < 1): #{
            print("[ERR ] Failed to retrieve any more data");
            #break;
            print("RETURNING: ", False, ", ", req, ", ", headers, ", ", body);
            return False, req, headers, body;
        #}

        print("4");
        if (len(body) + len(more) > size_max_http_total): #{
            print("[ERR ] HTTP payload beyond max: "
                + str(len(body) + len(more))
                + " > " + str(size_max_http_total)
            );

            yield from writer.awrite("HTTP/1.0 413 Payload Too Large\r\n\r\n");
            #yield from writer.aclose();
            print("RETURNING: ", False, ", ", req, ", ", headers, ", ", body);
            return False, req, headers, body;
        #}

        print("5");
        body = body + more;

        # Do we still need to get our headers?
        if (len(req) == 0): #{
            # Haven't split anything yet

            print("6");
            # Have we at least got the headers?
            try: #{
                firstbit, body = body.split('\r\n\r\n', 1);

                # Yep

                try: #{
                    req, firstbit = firstbit.split('\r\n', 1);
                except ValueError: #}{
                    req = firstbit;
                    firstbit = '';
                #}

                headers = firstbit.split('\r\n');
                firstbit = None;

                print("REQUEST1: ", req);
                # req     = [str] request (ie. "GET /puppy.png HTTP/1.1")
                # headers = [arr] array of [str] header items
                # body    = [str] body

                keys = ['method', 'uri', 'protocol'];
                req = req.split();
                if (len(req) < 3 or len(req) > 4): #{
                    print("[ERR ] HTTP Bad Request: Request not 3 elements: ", req);
                    yield from writer.awrite("HTTP/1.0 400 Bad Request\r\n\r\n");
                    #yield from writer.aclose();
                    return False, {}, {}, body;
                #}
                req = dict(zip(keys, req));

                # req     = [dict] of [str] request parts
                #           (ie. ["method" = "GET", "uri" = "/puppy.png", "protocol" = "HTTP/1.1"])
                print("REQUEST2: ", req);

                # dict-ify the header pair array
                try: #{
                    headers = dict(map(lambda s : map(str.strip, s.split(':', 1)), headers));
                except: #}{
                    print("[ERR ] HTTP Bad Request: Failed to dict-ifying headers: ", headers);
                    yield from writer.awrite("HTTP/1.0 400 Bad Request\r\n\r\n");
                    #yield from writer.aclose();
                    return False, {}, {}, body;
                #}

                # Lowercase the keys
                headers = dict((k.lower(), v) for k,v in headers.items());

                try: #{
                    clen = int(headers['content-length']);
                except: #}{
                    if not req['method'] == "POST": #{
                        # Doesn't (seem to) contain Content-Length so assume
                        # we're done and return?
                        break;
                    #}

                    print("[ERR ] HTTP Content-Length Required");

                    yield from writer.awrite("HTTP/1.0 411 Length Required\r\n\r\n");
                    #yield from writer.aclose();
                    return False, req, headers, body;
                #}
            except ValueError: #}{
                # No headers yet...
                pass;
            #}
        #}

        print("7");
        # Have we got Content-Length yet?
        if clen > 0: #{
            # And if we do, have we got MORE data than that?
            if len(body) > clen: #{
                print("[WARN] HTTP Content > Content-Length: "
                    + str(len(body))
                    + " > " + str(clen)
                );

            # And if we do, have we just the RIGHT amount of data?
            elif len(body) == clen: #}{
                # If we do, let's stop this loopy business
                break;
            #}

            # Continue until we read clen bytes of body
        #}

        # Continue until we get our headers and determine length of body
        print("8");
    #}

    print("10");
    #print("clen:    " + str(clen));
    #print("req:     " + req);
    #print("headers: " + str(headers));
    #print("body:    " + body);
    print("RETURNING: ", True, ", ", req, ", ", headers, ", ", body);
    return True, req, headers, body;
#}

@asyncio.coroutine
def serve(reader, writer): #{
    print("serve()");

    didread, req, headers, body = await read_complete_req(reader, writer);
    # [bool] didread   - Did it work
    # [dict] req       - The request:
    #   [str] method     - The request method
    #   [str] protocol   - The protocol (eg. "HTTP/1.1")
    #   [str] uri        - The URI      (eg. "/web_config.html")
    # [headers] read - Did it work
    # [bool] didread - Did it work
    if (not didread): #{
        # Failed to retrieve
        yield from writer.aclose();
        return;
    #}
    didread = None;
    headers = None;
    gc.collect();

    try: #{
        file, vardict = decode_path(req['uri']);
    except: #}{
        print("[ERR ] HTTP Bad Request: Failed to dict-ifying vararray for URI: ", req['uri']);
        yield from writer.awrite("HTTP/1.0 400 Bad Request\r\n\r\n");
        yield from writer.aclose();
        return;
    #}
    gc.collect();

    print("[" + req['method'] + "] Serving file: " + file + "(" + str(vardict) + ")");
    if exists(file): #{
        mime_type, cacheable = get_mime_type(file);

        if file.endswith(".py"): #{
            mod = None;

            print("EXECUTE:", file);

            if (not vardict): vardict = {};

            print("try1");
            try: #{
                modpath = file.rsplit(".", 1)[0];
                modname = modpath.rsplit("/", 1)[1];
                mod     = __import__(modpath);

            except: #}{
                yield from writer.awrite("HTTP/1.0 500 Internal Server Error: Exec1\r\n\r\n");
                yield from writer.aclose();
                gc.collect();
                return;
            #}

            print("try2:");
            print("\n\nmod:", mod);
            print("\n\nmodname:", modname);
            print("\n\nmethod:", req['method']);
            try: #{
                #modfunc = getattr(mod, modname);
                modfunc = getattr(mod, req['method']);

            except: #}{
                yield from writer.awrite("HTTP/1.0 500 Internal Server Error: Exec2\r\n\r\n");
                yield from writer.aclose();
                gc.collect();
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

            print("modfunc");

            # NOTE: You MUST output Content-Type and newline yourself in modfunc
            # funtions

            page = 1;
            morepages = True;
            while (morepages): #{
                buffer, morepages = modfunc(vardict, body, page);
                print("\n\n\nBUFFER[%d]:\n" % page);
                print(buffer, "\n\n\n");

                ####yield from writer.awrite("HTTP/1.0 200 OK\r\n");

                ##### FIXME: if buffer comes back as nothing (such as if I
                ##### async.sleep in the func) then write.awrite fails as buffer
                ##### is of type 'generator' and doesn't have .len()

                ###yield from writer.awrite(buffer);
                ##if (buffer): yield from writer.awrite(buffer);
                #if (buffer is not None): yield from writer.awrite(buffer);
                yield from writer.awrite(buffer.replace('\n', '\r\n'));

                page = page + 1;
            #}

            try: #{
                modfunc = getattr(mod, 'end' + req['method']);

            except: #}{
                yield from writer.aclose();
                gc.collect();
                return;
            #}

            page = 1;
            morepages = True;
            while (morepages): #{
                buffer, morepages = modfunc(vardict, body, page);

                ##### FIXME: if buffer comes back as nothing (such as if I
                ##### async.sleep in the func) then write.awrite fails as buffer
                ##### is of type 'generator' and doesn't have .len()

                yield from writer.awrite(buffer.replace('\n', '\r\n'));

                page = page + 1;
            #}

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
            gc.collect();
        #}
    else: #}{
        yield from writer.awrite("HTTP/1.0 404 Not Found\r\n\r\n");
    #}

    yield from writer.aclose();
    gc.collect();
#}

def start(): #{
    #KRAYON#import logging;
    #KRAYON#logging.basicConfig(level=logging.ERROR);

    print("Initialising event loop...");
    loop = asyncio.get_event_loop();
    print("Starting server...");
    loop.call_soon(asyncio.start_server(serve, "0.0.0.0", 80, 20));
    print("Entering loop...");
    loop.run_forever();
    loop.close();
#}

# vim:ts=4:tw=80:sw=4:et:ai:si
