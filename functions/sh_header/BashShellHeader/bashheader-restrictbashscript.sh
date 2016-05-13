#!/bin/sh

# Mode1: all line error will cause exit immediately
set -e
# set -e
    # Exit immediately if a pipeline (which may consist of a single simple command),  a subshell command enclosed in parentheses, or one  of  the  commands
    # executed as part of a command list enclosed by braces (see SHELL GRAMMAR above) exits with a non-zero status.  The shell does not exit if the command
    # that fails is part of the command list immediately following a while or until keyword, part of the test following the if or elif reserved words, part
    # of  any  command  executed in a && or ││ list except the command following the final && or ││, any command in a pipeline but the last, or if the com-
    # mand’s return value is being inverted with !.  A trap on ERR, if set, is executed before the shell exits.  This option applies to the shell  environ-
    # ment  and  each  subshell  environment separately (see COMMAND EXECUTION ENVIRONMENT above), and may cause subshells to exit before executing all the
    # commands in the subshell.

# Mode2: all line error will cause exit immediately AND all vars variable or parameter must be declared
set -eu
# set -e
    # Exit immediately if a pipeline (which may consist of a single simple command),  a subshell command enclosed in parentheses, or one  of  the  commands
    # executed as part of a command list enclosed by braces (see SHELL GRAMMAR above) exits with a non-zero status.  The shell does not exit if the command
    # that fails is part of the command list immediately following a while or until keyword, part of the test following the if or elif reserved words, part
    # of  any  command  executed in a && or ││ list except the command following the final && or ││, any command in a pipeline but the last, or if the com-
    # mand’s return value is being inverted with !.  A trap on ERR, if set, is executed before the shell exits.  This option applies to the shell  environ-
    # ment  and  each  subshell  environment separately (see COMMAND EXECUTION ENVIRONMENT above), and may cause subshells to exit before executing all the
    # commands in the subshell.
# set -u
    # Treat unset variables and parameters other than the special parameters "@" and "*" as an error when performing parameter expansion.  If expansion  is
    # attempted on an unset variable or parameter, the shell prints an error message, and, if not interactive, exits with a non-zero status.


# Following Mode1 or Mode2: refer to next comment
[ -n "$ENABLE_DEBUG_MODE" ] && set -x
# set -x
    # After  expanding  each  simple command, for command, case command, select command, or arithmetic for command, display the expanded value of PS4, fol-
    # lowed by the command and its expanded arguments or associated word list.
