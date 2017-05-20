reset # do not use any previous settings
set title "Candidate keyphrases extracted with PoS sequences (development corpus)" # title
set xlabel "Minimum number of ocurrences of each PoS sequence" # x-axis label
set ylabel "Precision/Recall/F1" # y-axis label
set term png size 1000, 600 font "Helvetica" 12
set size ratio 0.55 #plot dimensions
set output "posseq.png" # name of image file 
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

plot "dev_seq_projection_filter_by_count.dat" using 1:3:xtic(2) title "Precision" with linespoints ls 1, \
"dev_seq_projection_filter_by_count.dat" using 1:4:xtic(2) title "Recall" with linespoints ls 2, \
"dev_seq_projection_filter_by_count.dat" using 1:5:xtic(2) title "F1" with linespoints ls 3, \

reset # do not use any previous settings
set title "Candidate keyphrases extracted with RegExp (development corpus)" # title
set xlabel "Minimum number of ocurrences of each PoS sequence" # x-axis label
set ylabel "Precision/Recall/F1" # y-axis label
set term png size 1000, 600 font "Helvetica" 12
set size ratio 0.55 #plot dimensions
set output "regexp.png" # name of image file 
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

plot "dev_seq_regex_projection_filter_by_count.dat" using 1:3:xtic(2) title "Precision" with linespoints ls 1, \
"dev_seq_regex_projection_filter_by_count.dat" using 1:4:xtic(2) title "Recall" with linespoints ls 2, \
"dev_seq_regex_projection_filter_by_count.dat" using 1:5:xtic(2) title "F1" with linespoints ls 3, \

