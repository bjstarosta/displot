#!/bin/bash

# Run this script after editing .ui files in the /devel directory.
#
# It must be run from its own directory (CWD=.) so that the relative paths
# resolve as they're supposed to.
#
# Needs pyqt5-dev-tools if you're on *buntu, and equivalent everywhere else.

DIR="../displot/ui_def/"
PY_INIT=$DIR"__init__.py"
PREFIX="ui_"

strjoin() {
  [ "$#" -ge 1 ] || return 1
  local IFS="$1"
  shift
  printf '%s\n' "$*"
}

init='__all__ = ['
mods=()
for i in `find . -name '*.ui'`; do
  f="$PREFIX$(basename -s '.ui' $i)";
  mods+=('"'$f'"');
  echo "$DIR$f.py";
  pyuic5 $i -o "$DIR$f.py";
done
joined=$(strjoin , "${mods[@]}")
init+=$joined']'
echo $init > $PY_INIT
