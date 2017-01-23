reset # do not use any previous settings
set title "F1 score - Keyphrase extraction - Projection of POS sequences over the development data" # title
set xlabel "Min ocurrence of each POS sequence" # x-axis label
set ylabel "F1 score" # y-axis label
set term png size 1200, 700 font "Helvetica" 9
set size ratio 0.55 #plot dimensions
set output "plot_f1score.png" # name of image file 
set grid y
set xtics rotate
set ytics 0.01
set yrange [0.04:0.35] writeback
set key right top
set style data linespoints # set default way of data plotting
set pointsize 1.5 # increase size of points on the line

plot "dev_seq_projection_filter_by_count.dat" using 1:5:xtic(2) title "Simple projection", \
"dev_seq_projection_filter_by_count_inkeywords_not_indomains.dat" using 1:5 title "Keywords/DiscartingIfInOtherDomain", \
"dev_seq_projection_svm_only_anntokens_four_classes.dat" using 1:5 title "SVM/4c/AnnotatedTokens", \
"dev_seq_projection_svm_only_anntokens_four_classes_cossimgt0.01.dat" using 1:5 title "SVM/4c/AnnotatedTokens/Sim>0.01", \
"dev_seq_projection_svm4c_not-none.and.maxsimgt0_or_maxsimeq0.dat" using 1:5 title "SVM/4c/AnnotatedTokens/NotNoneOrNotDecision", \
"dev_seq_projection_svm_only_anntokens_four_classes_morefeatures.dat" using 1:5 title "SVM/4c/AnnotatedTokens/MoreFeatures", \
"dev_seq_projection_svm_only_anntokens_two_classes.dat" using 1:5 title "SVM/2c/AnnotatedTokens", \
"dev_seq_projection_svm_only_anntokens_two_classes_cossimgt0.005.dat" using 1:5 title "SVM/2c/AnnotatedTokens/Sim>0.005", \
"dev_seq_projection_svm_only_anntokens_two_classes_cossimgt0.01.dat" using 1:5 title "SVM/2c/AnnotatedTokens/Sim>0.01", \
"dev_seq_projection_svm_shorttext_two_classes.dat" using 1:5 title "SVM/2c/ShortText", \
"dev_seq_projection_svm_fulltext_two_classes.dat" using 1:5 title "SVM/2c/FullText"

reset # do not use any previous settings
set title "Precision - Keyphrase extraction - Projection of POS sequences over the development data" # title
set xlabel "Min ocurrence of each POS sequence" # x-axis label
set ylabel "Precision" # y-axis label
set term png size 1200, 700 font "Helvetica" 9
set size ratio 0.55 #plot dimensions
set output "plot_precision.png" # name of image file 
set grid y
set xtics rotate
set ytics 0.01
set yrange [0.04:0.35] writeback
set key right top
set style data linespoints # set default way of data plotting
set pointsize 1.5 # increase size of points on the line
plot "dev_seq_projection_filter_by_count.dat" using 1:3:xtic(2) title "Simple projection", \
"dev_seq_projection_filter_by_count_inkeywords_not_indomains.dat" using 1:3 title "Keywords/DiscartingIfInOtherDomain", \
"dev_seq_projection_svm_only_anntokens_four_classes.dat" using 1:3 title "SVM/4c/AnnotatedTokens", \
"dev_seq_projection_svm_only_anntokens_four_classes_cossimgt0.01.dat" using 1:3 title "SVM/4c/AnnotatedTokens/Sim>0.01", \
"dev_seq_projection_svm4c_not-none.and.maxsimgt0_or_maxsimeq0.dat" using 1:3 title "SVM/4c/AnnotatedTokens/NotNoneOrNotDecision", \
"dev_seq_projection_svm_only_anntokens_four_classes_morefeatures.dat" using 1:3 title "SVM/4c/AnnotatedTokens/MoreFeatures", \
"dev_seq_projection_svm_only_anntokens_two_classes.dat" using 1:3 title "SVM/2c/AnnotatedTokens", \
"dev_seq_projection_svm_only_anntokens_two_classes_cossimgt0.005.dat" using 1:3 title "SVM/2c/AnnotatedTokens/Sim>0.005", \
"dev_seq_projection_svm_only_anntokens_two_classes_cossimgt0.01.dat" using 1:3 title "SVM/2c/AnnotatedTokens/Sim>0.01", \
"dev_seq_projection_svm_shorttext_two_classes.dat" using 1:3 title "SVM/2c/ShortText", \
"dev_seq_projection_svm_fulltext_two_classes.dat" using 1:3 title "SVM/2c/FullText"

reset # do not use any previous settings
set title "Recall - Keyphrase extraction - Projection of POS sequences over the development data" # title
set xlabel "Min ocurrence of each POS sequence" # x-axis label
set ylabel "Recall" # y-axis label
set term png size 1200, 700 font "Helvetica" 9
set size ratio 0.55 #plot dimensions
set output "plot_recall.png" # name of image file 
set grid y
set xtics rotate
set ytics 0.05
set yrange [0.05:1.0] writeback
set key right top
set style data linespoints # set default way of data plotting
set pointsize 1.5 # increase size of points on the line

plot "dev_seq_projection_filter_by_count.dat" using 1:4:xtic(2) title "Simple projection", \
"dev_seq_projection_filter_by_count_inkeywords_not_indomains.dat" using 1:4 title "Keywords/DiscartingIfInOtherDomain", \
"dev_seq_projection_svm_only_anntokens_four_classes.dat" using 1:4 title "SVM/4c/AnnotatedTokens", \
"dev_seq_projection_svm_only_anntokens_four_classes_cossimgt0.01.dat" using 1:4 title "SVM/4c/AnnotatedTokens/Sim>0.01", \
"dev_seq_projection_svm4c_not-none.and.maxsimgt0_or_maxsimeq0.dat" using 1:4 title "SVM/4c/AnnotatedTokens/NotNoneOrNotDecision", \
"dev_seq_projection_svm_only_anntokens_four_classes_morefeatures.dat" using 1:4 title "SVM/4c/AnnotatedTokens/MoreFeatures", \
"dev_seq_projection_svm_only_anntokens_two_classes.dat" using 1:4 title "SVM/2c/AnnotatedTokens", \
"dev_seq_projection_svm_only_anntokens_two_classes_cossimgt0.005.dat" using 1:4 title "SVM/2c/AnnotatedTokens/Sim>0.005", \
"dev_seq_projection_svm_only_anntokens_two_classes_cossimgt0.01.dat" using 1:4 title "SVM/2c/AnnotatedTokens/Sim>0.01", \
"dev_seq_projection_svm_shorttext_two_classes.dat" using 1:4 title "SVM/2c/ShortText", \
"dev_seq_projection_svm_fulltext_two_classes.dat" using 1:4 title "SVM/2c/FullText"
