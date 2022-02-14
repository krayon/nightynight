import os;

# Quick check if a file exists
def exists(file): #{
    try: #{
        s = os.stat(file);
        return True;
    except: #}{
        return False;
    #}
#}

# vim:ts=4:tw=80:sw=4:et:ai:si
