#!/usr/bin/env bash
# Usage: bash $0
# Author: dgden
# Create Date: 2021/4/25
# Create Time: 13:57
# Description: remove files or directories safely on Linux

if [[ -f "$HOME"/.bashrc ]]; then
  bash_rc_path="$HOME"/.bashrc
elif [[ -f "$HOME"/.bash_profile ]]; then
  bash_rc_path="$HOME"/.bash_profile
fi

\cp "$bash_rc_path" "${bash_rc_path}_$(date +%Y%m%d%H%M%S)~"

cat >>"$bash_rc_path" <<'eof'
# enable trash bin for bash
if [ ! -d ~/.trash ]; then
  mkdir -p ~/.trash
fi

alias rm=trash
alias r=trash
alias rl='ls ~/.trash'
alias ur=undelete_file
alias cr=clear_trash
undelete_file() {
  mv -i ~/.trash/"$*" ./
}

trash() {
  mv "$@" ~/.trash/
}

clear_trash() {
  read -pr "clear sure?[n]" confirm
  [ "$confirm" == 'y' ] || [ "$confirm" == 'Y' ] && /usr/bin/rm -rf ~/.trash/*
}
# end


eof

# shellcheck source=$HOME/.bashrc
source "$HOME"/.bashrc

echo "Tips: use a separate disk or mount point to serve the important files, so you can use extundelete easily."

# shellcheck disable=SC2028
echo 'You can use "\rm -rf path" to delete directly.'
