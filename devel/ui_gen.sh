#!/bin/bash

# Run this script after editing .ui files in the /devel directory.
#
# It must be run from its own directory (CWD=.) so that the relative paths
# resolve as they're supposed to.
#
# Needs pyqt5-dev-tools if you're on *buntu, and equivalent (that contains
# pyuic5 and pyrcc5) everywhere else.

DIR="../displot/ui/"
PY_INIT=$DIR"__init__.py"
PREFIX="ui_"
SUFFIX="_rc"

# layout files
for i in `find . -name '*.ui'`; do
  f="$PREFIX$(basename -s '.ui' $i)";
  echo "$DIR$f.py";
  pyuic5 $i -o "$DIR$f.py" --from-imports;

  # get rid of a bugged piece of code
  sed -i -e 's/QtCore.QMetaObject.connectSlotsByName/#QtCore.QMetaObject.connectSlotsByName/g' "$DIR$f.py"
done

# resource files
for i in `find . -name '*.qrc'`; do
  f="$(basename -s '.qrc' $i)$SUFFIX";
  echo "$DIR$f.py";
  pyrcc5 $i -o "$DIR$f.py";
done
