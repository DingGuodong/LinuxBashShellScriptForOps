# delete some string from string
    # one line
    sed -r 's/information_schema ?| ?mysql ?//g'
    # several row
    grep -Eiv '(database|information_schema|performance_schema|mysql)')

# string replace
    # using bash buildin
    # refer to http://www.gnu.org/software/bash/manual/bashref.html#Shell-Parameters
    # ${parameter/pattern/string}
    touch 2009abcd001{1..10}001.mhi
    for file in `ls 2009abcd001*.mhi`; do mv $file "`echo ${file//001.mhi/002.mhi}`"; done

    # using sed
    echo '001.mhi' | sed 's/001.mhi/002.mhi/g'

    # using awk
    echo '001.mhi' | awk 'gsub('001.mhi','002.mhi') {print $0}'

    # python
    str.replace()
    re.sub()