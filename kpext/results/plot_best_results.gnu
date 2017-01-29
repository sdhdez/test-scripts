reset # do not use any previous settings
set title "F1 score - Keyphrase extraction - Projection of POS sequences over the development data" # title
set xlabel "Min ocurrence of each POS sequence" # x-axis label
set ylabel "F1 score" # y-axis label
set term png size 1200, 700 font "Helvetica" 9
set size ratio 0.55 #plot dimensions
set output "plot_f1score.png" # name of image file 
set grid y
set xtics rotate
set ytics 0.02
set yrange [0.04:0.50] writeback
set key right top
set style data linespoints # set default way of data plotting
set pointsize 1.5 # increase size of points on the line

plot "dev_seq_projection_filter_by_count.dat" using 1:5:xtic(2) title "Simple projection", \
"dev_seq_projection_crf_train_with_projections_simple.dat" using 1:5 title "CRF/POSseq/Simple", \
"dev_seq_projection_crf_train_with_projections_largest.dat" using 1:5 title "CRF/POSseq/Largest", \
"dev_seq_projection_crf_train_with_projections_by_class.dat" using 1:5 title "CRF/POSseq/Simple/ByType", \
"dev_seq_projection_crf_train_with_projections_largest_by_class.dat" using 1:5 title "CRF/POSseq/Largest/ByType", \
"dev_seq_projection_crf_train_with_projections_largest_over_results_svm2c_fulltext.dat" using 1:5 title "CRF/POSseq/Largest/SVM2cFullText", \
"dev_seq_projection_crf_train_with_projections_without_types.dat" using 1:5 title "CRF/POSseq/Simple/WithoutType", \
"dev_seq_projection_crf_train_with_projections_largest_without_types.dat" using 1:5 title "CRF/POSseq/Largest/WithoutType", \
0.291463414634 title "CRF"

reset # do not use any previous settings
set title "Precision - Keyphrase extraction - Projection of POS sequences over the development data" # title
set xlabel "Min ocurrence of each POS sequence" # x-axis label
set ylabel "Precision" # y-axis label
set term png size 1200, 700 font "Helvetica" 9
set size ratio 0.55 #plot dimensions
set output "plot_precision.png" # name of image file 
set grid y
set xtics rotate
set ytics 0.02
set yrange [0.04:0.50] writeback
set key right top
set style data linespoints # set default way of data plotting
set pointsize 1.5 # increase size of points on the line

plot "dev_seq_projection_filter_by_count.dat" using 1:3:xtic(2) title "Simple projection", \
"dev_seq_projection_crf_train_with_projections_simple.dat" using 1:3 title "CRF/POSseq/Simple", \
"dev_seq_projection_crf_train_with_projections_largest.dat" using 1:3 title "CRF/POSseq/Largest", \
"dev_seq_projection_crf_train_with_projections_by_class.dat" using 1:3 title "CRF/POSseq/Simple/ByType", \
"dev_seq_projection_crf_train_with_projections_largest_by_class.dat" using 1:3 title "CRF/POSseq/Largest/ByType", \
"dev_seq_projection_crf_train_with_projections_largest_over_results_svm2c_fulltext.dat" using 1:3 title "CRF/POSseq/Largest/SVM2cFullText", \
"dev_seq_projection_crf_train_with_projections_without_types.dat" using 1:3 title "CRF/POSseq/Simple/WithoutType", \
"dev_seq_projection_crf_train_with_projections_largest_without_types.dat" using 1:3 title "CRF/POSseq/Largest/WithoutType", \
0.491769547325 title "CRF"

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
"dev_seq_projection_crf_train_with_projections_simple.dat" using 1:4 title "CRF/POSseq/Simple", \
"dev_seq_projection_crf_train_with_projections_largest.dat" using 1:4 title "CRF/POSseq/Largest", \
"dev_seq_projection_crf_train_with_projections_by_class.dat" using 1:4 title "CRF/POSseq/Simple/ByType", \
"dev_seq_projection_crf_train_with_projections_largest_by_class.dat" using 1:4 title "CRF/POSseq/Largest/ByType", \
"dev_seq_projection_crf_train_with_projections_largest_over_results_svm2c_fulltext.dat" using 1:4 title "CRF/POSseq/Largest/SVM2cFullText", \
"dev_seq_projection_crf_train_with_projections_without_types.dat" using 1:4 title "CRF/POSseq/Simple/WithoutType", \
"dev_seq_projection_crf_train_with_projections_largest_without_types.dat" using 1:4 title "CRF/POSseq/Largest/WithoutType", \
0.207105719237 title "CRF"
