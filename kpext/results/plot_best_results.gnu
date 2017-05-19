reset # do not use any previous settings
set title "F1 score - Keyphrase identification with the development corpus" # title
set xlabel "Minimum number of ocurrences of each PoS sequence" # x-axis label
set ylabel "F1 score" # y-axis label
set term png size 1000, 600 font "Helvetica" 12
set size ratio 0.55 #plot dimensions
set output "f1score.png" # name of image file 
set grid y
set xtics rotate
set format y "%1.2f";
set ytics 0.05
set yrange [0.0:0.40] writeback
set key right top
set style data linespoints # set default way of data plotting
set pointsize 1.3 # increase size of points on the line
set style line 1 lc rgb '#0060ad' pt 5   # square
set style line 2 lc rgb '#dd181f' pt 7   # circle
set style line 3 lc rgb '#2E8B57' pt 9   # triangle
set style line 4 lw 1.5 lc rgb '#6495ED' pt 1
set style line 5 lw 1.5 lc rgb '#FF1493' pt 1   


plot "dev_seq_projection_filter_by_count.dat" using 1:5:xtic(2) title "Candidate keyphrases" with linespoints ls 3, \
"dev_seq_projection_crf_train_with_projections_largest_without_types.dat" using 1:5 title "Candidate keyphrases + CRF" with linespoints ls 1, \
"dev_seq_projection_crf_train_with_projections_largest_without_types_msag_boolean.dat" using 1:5 title "Candidate keyphrases + CRF + Titles" with linespoints ls 2, \
0.291463414634 title "CRF" with line ls 4, \
0.293939393939 title "CRF + Titles" with line ls 5

#0.283656509695 title "CRF/MSAG", \
#"dev_seq_projection_crf_train_with_projections_largest.dat" using 1:5 title "CRF/POSseq/Largest", \
#"dev_seq_projection_crf_train_with_projections_largest_msag.dat" using 1:5 title "CRF/POSseq/Largest/MSAG", \
#"dev_seq_projection_crf_train_with_projections_largest_without_types_msag.dat" using 1:5 title "CRF/POSseq/Largest/WithoutType/MSAG", \
#"dev_seq_projection_crf_train_with_projections_simple.dat" using 1:5 title "CRF/POSseq/Simple", \
#"dev_seq_projection_crf_train_with_projections_largest_by_class.dat" using 1:5 title "CRF/POSseq/Largest/ByType", \

reset # do not use any previous settings
set title "Precision - Keyphrase identification with the development corpus" # title
set xlabel "Minimum number of ocurrences of each PoS sequence" # x-axis label
set ylabel "Precision" # y-axis label
set term png size 1000, 600 font "Helvetica" 12
set size ratio 0.55 #plot dimensions
set output "precision.png" # name of image file 
set grid y
set xtics rotate
set format y "%1.2f";
set ytics 0.1
set yrange [0.0:0.50] writeback
set key right top
set style data linespoints # set default way of data plotting
set pointsize 1.3 # increase size of points on the line
set style line 1 lc rgb '#0060ad' pt 5   # square
set style line 2 lc rgb '#dd181f' pt 7   # circle
set style line 3 lc rgb '#2E8B57' pt 9   # triangle
set style line 4 lw 1.5 lc rgb '#6495ED' pt 1
set style line 5 lw 1.5 lc rgb '#FF1493' pt 1   



plot "dev_seq_projection_filter_by_count.dat" using 1:3:xtic(2) title "Candidate keyphrases" with linespoints ls 3, \
"dev_seq_projection_crf_train_with_projections_largest_without_types.dat" using 1:3 title "Candidate keyphrases + CRF" with linespoints ls 1, \
"dev_seq_projection_crf_train_with_projections_largest_without_types_msag_boolean.dat" using 1:3 title "Candidate keyphrases + CRF + Titles" with       linespoints ls 2, \
0.491769547325 title "CRF" with line ls 4, \
0.352300242131 title "CRF + Titles" with line ls 5
#"dev_seq_projection_crf_train_with_projections_simple.dat" using 1:3 title "CRF/POSseq/Simple", \
#"dev_seq_projection_crf_train_with_projections_largest_by_class.dat" using 1:3 title "CRF/POSseq/Largest/ByType", \
#"dev_seq_projection_crf_train_with_projections_largest_msag.dat" using 1:3 title "CRF/POSseq/Largest/MSAG", \
#"dev_seq_projection_crf_train_with_projections_largest_without_types_msag.dat" using 1:3 title "CRF/POSseq/Largest/WithoutType/MSAG", \
#"dev_seq_projection_crf_train_with_projections_largest.dat" using 1:3 title "CRF/POSseq/Largest", \
#0.393241167435 title "CRF/MSAG", \

reset # do not use any previous settings
set title "Recall - Keyphrase identification with the development corpus" # title
set xlabel "Minimum number of ocurrences of each PoS sequence" # x-axis label
set ylabel "Recall" # y-axis label
set term png size 1000, 600 font "Helvetica" 12
set size ratio 0.55 #plot dimensions
set output "recall.png" # name of image file 
set grid y
set xtics rotate
set format y "%1.2f";
set ytics 0.1
set yrange [0.0:1.0] writeback
set key right top
set style data linespoints # set default way of data plotting
set pointsize 1.3 # increase size of points on the line
set style line 1 lc rgb '#0060ad' pt 5   # square
set style line 2 lc rgb '#dd181f' pt 7   # circle
set style line 3 lc rgb '#2E8B57' pt 9   # triangle
set style line 4 lw 1.5 lc rgb '#6495ED' pt 1
set style line 5 lw 1.5 lc rgb '#FF1493' pt 1   

plot "dev_seq_projection_filter_by_count.dat" using 1:4:xtic(2) title "Candidate keyphrases" with linespoints ls 3, \
"dev_seq_projection_crf_train_with_projections_largest_without_types.dat" using 1:4 title "Candidate keyphrases + CRF" with linespoints ls 1, \
"dev_seq_projection_crf_train_with_projections_largest_without_types_msag_boolean.dat" using 1:4 title "Candidate keyphrases + CRF + Titles" with linespoints ls 2, \
0.207105719237 title "CRF" with line ls 4, \
0.252166377816 title "CRF + Titles" with line ls 5
#"dev_seq_projection_crf_train_with_projections_simple.dat" using 1:4 title "CRF/POSseq/Simple", \
#"dev_seq_projection_crf_train_with_projections_largest_by_class.dat" using 1:4 title "CRF/POSseq/Largest/ByType", \
#"dev_seq_projection_crf_train_with_projections_largest_msag.dat" using 1:4 title "CRF/POSseq/Largest/MSAG", \
#"dev_seq_projection_crf_train_with_projections_largest_without_types_msag.dat" using 1:4 title "CRF/POSseq/Largest/WithoutType/MSAG", \
#"dev_seq_projection_crf_train_with_projections_largest.dat" using 1:4 title "CRF/POSseq/Largest", \
#0.221837088388 title "CRF/MSAG", \
