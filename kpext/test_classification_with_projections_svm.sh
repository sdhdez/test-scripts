#!/bin/bash

TRAIN_DIR=$1;
PROJECTIONS_DIR=$2;
OUTPUT_DIR=$3;

EVAL_SCRIPT=$4;
EVAL_RESULTS_FILE="evaluation_results_tmp.dat";

TEST_DIR=$5;

DEBUG="";

if [ ! -d $OUTPUT_DIR ]
then
    mkdir $OUTPUT_DIR;
fi

if [ -f $EVAL_RESULTS_FILE ]
then 
    echo $EVAL_RESULTS_FILE " already exists."
    if [[ ! $DEBUG == "debug" ]]
    then 
        exit;
    fi
fi

echo "#Id FilterMinCount precision recall f1score" >> $EVAL_RESULTS_FILE;
echo "#Id FilterMinCount precision recall f1score" >> $EVAL_RESULTS_FILE".2";

tmp_last_count="";
current_index=0;
while read pos_seq_count CUR_PROJECTION
do
    if [[ $tmp_last_count != $pos_seq_count ]]
    then
        ((current_index++));
        FULL_NEW_PATH=$OUTPUT_DIR"pos_seq_count_gt"$pos_seq_count;
        if [ ! -d $FULL_NEW_PATH ]
        then
            mkdir $FULL_NEW_PATH;
        fi

        if [ -d $FULL_NEW_PATH ]
        then
            PROJECTION=$PROJECTIONS_DIR$CUR_PROJECTION
            python kp_svm_with_projection_four_classes.py $TRAIN_DIR $PROJECTION $FULL_NEW_PATH $DEBUG;
            read foo precision recall f1score total < <(python $EVAL_SCRIPT $TEST_DIR $FULL_NEW_PATH types | grep "KEYPHRASE");
            echo $current_index $pos_seq_count $precision $recall $f1score >> $EVAL_RESULTS_FILE;
            read foo foo foo precision recall f1score total < <(python $EVAL_SCRIPT $TEST_DIR $FULL_NEW_PATH rel | grep "total");
            echo $current_index $pos_seq_count $precision $recall $f1score >> $EVAL_RESULTS_FILE".2";
        fi
        if [[ $DEBUG == "debug" ]]
        then 
            break;
        fi
    fi
    tmp_last_count=$pos_seq_count;
done < <(ls -1 $PROJECTIONS_DIR | sed -e 's/\(pos_seq_count_gt\([0-9]\+\)\)/\2 \1/' | sort -n)
