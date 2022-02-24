import os;
import globs;

# Returns:
#   <s:buffer>, <i:next_offset>
def web_reboot(size_buf, offset, vardict, body): #{
    print("web_reboot.web_reboot(size_buf:%d, offset:%d, vardict, body)" % (size_buf, offset));
    return "", -1;
#}

# Returns:
#   <s:buffer>, <i:next_offset>
def GET(size_buf, offset, vardict, body): #{
    print("web_reboot.GET(size_buf:%d, offset:%d, vardict, body)" % (size_buf, offset));

    buf    = '';
    read   =  0;

    title = globs.prod + " " + globs.desc;

    try: #{
        f = open('web_reboot.pyhtml', 'rb');
    except: #}{
        print('[ERR ] Template not found');
        return "HTTP/1.0 404 Not Found\n\n", -1;
    #}

    output = '';
    if (offset <= 0): #{
        output = "HTTP/1.0 200 OK\nContent-Type: text/html\n\n";
    else: #}{
        f.seek(offset);
    #}

    # TODO: Handle if we only get half a encoded tag better ("<?py ... ?>")
    #       For now, we skip the tag :facepalm:

    code_s = 99;
    code_e = -1;
    while (code_s >= 0 and code_e < 0): #{
        offset = offset + read;
        buf = f.read(size_buf - len(output));
        buf = buf.decode();
        read = len(buf);
        if (read == 0): #{
            # We're done
            f.close(); f = None;
            return output, -1;
        #}
        code_s = buf.find('<?py');
        code_e = buf.find('?>');
    #}

    # If there's no "<?py", just put it straight through
    if (code_s < 0): #{
        f.close(); f = None;
        return output + buf, offset + read;
    #}

    # If there's a "<?py" later in the string, output everything up to that
    if (code_s > 0): #{
        f.close(); f = None;
        print('Breaking at py tag');
        return output + buf[:code_s], offset + code_s;
    #}

    # Starting with code tag
    #offset = offset + code_e;
    buf = buf[4:code_e].strip();
    code_s = None;
    #code_e = None;
    read = 0;

    print("Processing py tag:|" + buf + "|");
    buf = eval(buf, {'title': title});

    f.close(); f = None;
    return buf, offset + code_e + 2;
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
