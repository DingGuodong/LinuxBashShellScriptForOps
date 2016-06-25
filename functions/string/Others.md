# delete some string from string
    # one line
    sed -r 's/information_schema ?| ?mysql ?//g'
    # several row
    grep -Eiv '(database|information_schema|performance_schema|mysql)')
