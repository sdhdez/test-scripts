#!/bin/bash

EVAL_SCRIPT=$1;
TEST_DIR=$2;
RESULTS_DIR=$3;
SUBTASKB="$4";
EVAL_RESULTS_FILE="evaluation_results_tmp.dat$5";

DEBUG="";

if [ -f $EVAL_RESULTS_FILE ] || [ -f $EVAL_RESULTS_FILE".2" ]
then 
    echo $EVAL_RESULTS_FILE " already exists."
    if [[ ! $DEBUG == "debug" ]]
    then 
        exit;
    fi
fi

echo "#Id FilterMinCount precision recall f1score" >> $EVAL_RESULTS_FILE;

if [[ $SUBTASKB != "" ]]
then 
    echo "#Id FilterMinCount precision recall f1score" >> $EVAL_RESULTS_FILE".2";
fi

tmp_last_count="";
current_index=0;
while read pos_seq_count CUR_PROJECTION
do
    if [[ $tmp_last_count != $pos_seq_count ]]
    then
        ((current_index++));
        RESULT_PATH=$RESULTS_DIR"/pos_seq_count_gt"$pos_seq_count;
        if [ -d $RESULT_PATH ]
        then
            echo $RESULT_PATH;
            read foo precision recall f1score < <(python $EVAL_SCRIPT $TEST_DIR $RESULT_PATH types | grep "KEYPHRASE");
            echo $current_index $pos_seq_count $precision $recall $f1score >> $EVAL_RESULTS_FILE;
            if [[ $SUBTASKB != "" ]]
            then 
                read foo precision recall f1score < <(python $EVAL_SCRIPT $TEST_DIR $RESULT_PATH rel | grep "all_micro");
                echo $current_index $pos_seq_count $precision $recall $f1score >> $EVAL_RESULTS_FILE".2";
            fi
        fi
        if [[ $DEBUG == "debug" ]]
        then 
            break;
        fi
    fi
    tmp_last_count=$pos_seq_count;
done < <(ls -1 $RESULTS_DIR | sed -e 's/\(pos_seq_count_gt\([0-9]\+\)\)/\2 \1/' | sort -n)
