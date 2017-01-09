#!/bin/bash
# delete all spaces and comments of specialized file, using with $@ filename

DEBUG=false

if ${DEBUG} ; then
    old_PS4=$PS4  # system builtin variable does not need '${var}' expression
#    export PS4='+${BASH_SOURCE}:${LINENO}:${FUNCNAME[0]}: '
    export PS4='+${LINENO}: ${FUNCNAME[0]}: ' # if there is only one bash script, do not display ${BASH_SOURCE}
    _XTRACE_FUNCTIONS=$(set +o | grep xtrace)
    set -o xtrace
fi

function is_file_exist(){
    test -f $1 || echo "ls: cannot access $file: No such file or directory" && exit 1
}

function dos2unix_text_file_format_converter(){
    if cat -A ${file} | grep '\^M\\$' >/dev/null || file ${file} | grep "with CRLF line terminators" >/dev/null ; then
        which dos2unix >/dev/null 2>&1 || yum -q -y install dos2unix || apt-get -qq -y install dos2unix
        dos2unix ${file} >/dev/null
    fi
}

function del_comment_in_c_cpp_file(){
    tmp_file=/tmp/.noComment_$(date +%Y%m%d%H%M%S%N$RANDOM)
    cp ${file} ${tmp_file}

    #delete the comment line begin with '//comment'
    sed -i "/^[ \t]*\/\//d" ${tmp_file}

    #delete the comment line end with '//comment'
    sed -i "s/\/\/[^\"]*//" ${tmp_file}

    #delete the comment only occupied one line '/* comment */'
    sed -i "s/\/\*.*\*\///" ${tmp_file}

    #delete the comment that occupied many lines '/*comment
    #                                              *comment
    #                                              */
    sed -i "/^[ \t]*\/\*/,/.*\*\//d" ${tmp_file}

    grep -v ^$ ${tmp_file}

    \rm -f ${tmp_file}
}

function del_comment_in_sh_conf_file(){
    #ignore the comment line end with '# comment'
    grep -v "^[ \t]*\#" ${file} | grep -v "^$"
#    grep -vP "^[ \t]*\#|^$" ${file}
#    grep -vP "^\s\#|^$" ${file}  #Perl regular expressions give additional functionality, and are documented in
    # pcresyntax(3)  and pcrepattern(3), but only work if pcre is available in the system.

}

function del_comment_in_xml_file(){
    if test -f ${file} && file ${file} | grep "XML" >/dev/null; then
        which tidy >/dev/null 2>&1 || yum -q -y install tidy >/dev/null 2>&1 || apt-get -qq -y install tidy >/dev/null 2>&1
        tidy -quiet -asxml -xml -indent -wrap 1024 --hide-comments 1 ${file}
    else
        which tidy >/dev/null 2>&1 || yum -q -y install tidy >/dev/null 2>&1 || apt-get -qq -y install tidy >/dev/null 2>&1
        tidy -quiet -asxml -xml -indent -wrap 1024 --hide-comments 1 ${file}
    fi
}

function del_comment_in_general_file(){
    #ignore the comment line end with '# comment'
    grep -v "^[ \t]*\#" ${file} | grep -v "^[ \t]*\;" |grep -v "^$"
    # TODO(Guodong Ding) comment style in python using ''', """
}


function del_comment(){
    case ${file} in
        *.c|*.cpp|*.h)
            del_comment_in_c_cpp_file
            ;;
        *.sh|*.conf)
            del_comment_in_sh_conf_file
            ;;
        *.xml)
            del_comment_in_xml_file
            ;;
        *)
            del_comment_in_general_file
            ;;
    esac
}

file=$1
if [[ -f ${file} ]]; then
    del_comment
else
    echo "ls: cannot access $file: No such file or directory" && exit 1
fi

if ${DEBUG} ; then
    export PS4=${old_PS4}
    ${_XTRACE_FUNCTIONS}
fi
