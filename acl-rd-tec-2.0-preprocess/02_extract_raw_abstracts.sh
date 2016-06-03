#!/bin/bash 

EXPLORE_DIR=$1
EXPORT_DIR=$2;

if [[ -d "$2" ]]; then
  echo "Make sure that the EXPORT_DIR doesn't exists." >&2;
  exit;
else
  mkdir $EXPORT_DIR;
fi 

for f in `find $EXPLORE_DIR -type f`; do 
  FULL_DIRPATH=$EXPORT_DIR"/"${f%/*};
  TMP_FILENAME=$FULL_DIRPATH"/"${f##*/};
  mkdir -p $FULL_DIRPATH;
  FULL_FILENAME=${TMP_FILENAME%.xml}"_abstract.txt";
  cat $f | grep -E "<S>" | sed -e 's%<S>%%g' -e 's%<\/S>%\n%g' > $FULL_FILENAME;
done
