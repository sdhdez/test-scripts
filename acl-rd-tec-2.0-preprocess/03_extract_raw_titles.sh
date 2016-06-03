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
  FULL_FILENAME=${TMP_FILENAME%.xml}"_titles.txt";
  cat $f | grep -E "<Title>" | sed -e 's%<Title>%%g' -e 's%<\/Title>%\n%g' > $FULL_FILENAME;
done
