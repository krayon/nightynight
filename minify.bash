#!/bin/bash

# strpad [-l] <n> <str>
strpad() {
    unset leftside
    [ "${1}" == "-l" ] && leftside=1 && shift 1

    n="${1}"; shift 1
    str="${1}"; shift 1

    # NaN
    [ "${n}" -eq "${n}" ] &>/dev/null || { echo "${n}" && return 1; }

    [ ${#str} -ge ${n} ] && echo "${str}" && return 0

    xtr="$((10 ** (${n} - ${#str})))"
    xtr="${xtr:1}"
    [ ! -z "${leftside}" ] && echo "${xtr//0/ }${str}" || echo "${str}${xtr//0/ }"
}

echo "Minifying files..."

inw=0
sizw=0
for fin in *SOURCE.html *SOURCE.css; do #{
    inw2="${#fin}"
    [ ${inw2} -gt ${inw} ] && inw=${inw2}

    sizw2=$(stat -c %s "${fin}"); sizw2="${#sizw2}"
    [ ${sizw2} -gt ${sizw} ] && sizw=${sizw2}
done #}
unset inw2
unset sizw2

onw=$((${inw} + 2))

for fin in *SOURCE.html *SOURCE.css; do #{
    finsize=$(stat -c %s "${fin}")
    fout="${fin/SOURCE/MINIFIED}"
    echo -n "$(strpad -l ${inw} "${fin}") ($(strpad -l ${sizw} ${finsize})) -->"
    [ "${fin: -5}" == ".html" ] && {
        tr '\n' ' ' <"${fin}"|sed 's#[ \t]\+# #g;s#> <#><#g' >"${fout}"
    } || [ "${fin: -4}" == ".css" ] && {
        tr '\n' ' ' <"${fin}"|sed 's#[ \t]\+# #g;s#/\*[^\*]*\*/##g' >"${fout}"
    }

    foutsize=$(stat -c %s "${fout}")
    echo -n " $(strpad -l ${onw} "${fout}") ($(strpad -l ${sizw} ${foutsize}))"
    echo ":$(strpad -l 3 "$((100 - (${foutsize}00 / ${finsize})))")% reduced"
done #}



# vim:set ts=4 sw=4 tw=80 et ai si:
