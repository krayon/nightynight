# Handling pyhtml (html with '<?py ... ?>' eval tags)

# Returns:
#   <b:pyhtml_code> <s:buffer>, <i:next_offset>
#
# TODO: Support alternative headers and return codes
def pyhtml_parser(pyhtml_file, size_buf, offset, vardict, body): #{
    print("pyhtml_parser(size_buf:%d, offset:%d, vardict, body)" % (size_buf, offset));

    buf    = '';
    read   =  0;

    try: #{
        f = open(pyhtml_file, 'rb');
    except: #}{
        print('[ERR ] Template not found');
        return False, "HTTP/1.0 404 Not Found\n\n", -1;
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
            return False, output, -1;
        #}
        code_s = buf.find('<?py');
        code_e = buf.find('?>');
    #}

    # If there's no "<?py", just put it straight through
    if (code_s < 0): #{
        f.close(); f = None;
        return False, output + buf, offset + read;
    #}

    # If there's a "<?py" later in the string, output everything up to that
    if (code_s > 0): #{
        f.close(); f = None;
        print('Breaking at py tag');
        return False, output + buf[:code_s], offset + code_s;
    #}

    # Starting with code tag
    #offset = offset + code_e;
    buf = buf[4:code_e].strip();
    code_s = None;
    #code_e = None;
    read = 0;

    f.close(); f = None;
    return True, buf, offset + code_e + 2;
#}

# vim:ts=4:tw=80:sw=4:et:ai:si
