#!/bin/bash

TEST_DIR=$1;
OUTPUT_DIR=$2;
POS_TAGS_FILE=$3;

EVAL_SCRIPT=$4;
EVAL_RESULTS_FILE="evaluation_results_tmp.dat";


if [ ! -d $OUTPUT_DIR ]
then
    mkdir $OUTPUT_DIR;
fi

if [ -f $EVAL_RESULTS_FILE ]
then 
    echo $EVAL_RESULTS_FILE " already exists."
    exit;
fi

echo "#FilterMinCount precision recall f1score" >> $EVAL_RESULTS_FILE;

tmp_last_count="";
while read pos_seq_id pos_seq_count pos_tags
do
    if [[ $tmp_last_count != $pos_seq_count ]]
    then 
        FULL_NEW_PATH=$OUTPUT_DIR"pos_seq_count_gt"$pos_seq_count;
        if [ ! -d $FULL_NEW_PATH ]
        then
            mkdir $FULL_NEW_PATH;
        fi

        if [ -d $FULL_NEW_PATH ]
        then
            python kp_seq_projection.py $TEST_DIR $FULL_NEW_PATH $POS_TAGS_FILE $pos_seq_count;
            read foo precision recall f1score total < <(python $EVAL_SCRIPT $TEST_DIR $FULL_NEW_PATH types | grep "KEYPHRASE");
            echo $pos_seq_count $precision $recall $f1score >> $EVAL_RESULTS_FILE;
        fi
    fi
    tmp_last_count=$pos_seq_count;
done < $POS_TAGS_FILE




