#!/bin/bash

TRAIN_FILE=$1;
PROJECTIONS_DIR=$2;
OUTPUT_DIR="$3"$4;

DEBUG="";

if [ ! -d $OUTPUT_DIR ]
then
    mkdir $OUTPUT_DIR;
fi

tmp_last_count="";
current_index=0;
while read pos_seq_count CUR_PROJECTION
do
    if [[ $tmp_last_count != $pos_seq_count ]]
    then
        ((current_index++));
        FULL_NEW_PATH=$OUTPUT_DIR"/pos_seq_count_gt"$pos_seq_count;
        if [ ! -d $FULL_NEW_PATH ]
        then
            mkdir $FULL_NEW_PATH;
        fi

        if [ -d $FULL_NEW_PATH ]
        then
            PROJECTION=$PROJECTIONS_DIR$CUR_PROJECTION
            python kp_crfsuite_projection.py $PROJECTION $FULL_NEW_PATH $TRAIN_FILE;
        fi
        if [[ $DEBUG == "debug" ]]
        then 
            break;
        fi
    fi
    tmp_last_count=$pos_seq_count;
done < <(ls -1 $PROJECTIONS_DIR | sed -e 's/\(pos_seq_count_gt\([0-9]\+\)\)/\2 \1/' | sort -n)
