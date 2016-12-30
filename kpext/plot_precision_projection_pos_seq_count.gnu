reset # do not use any previous settings
set title "Precision - Keyphrase extraction - Projection of POS sequences over the development data" # title
set xlabel "Min ocurrence of each POS sequence" # x-axis label
set ylabel "Precision" # y-axis label
set term png size 800, 400 font "Helvetica" 10
set size ratio 0.4 #plot dimensions
set output "plot_precision_projection_pos_seq_count.png" # name of image file 
set grid y
set xtics rotate
set ytics 0.01
set key left top
set style data linespoints # set default way of data plotting
set pointsize 1.5 # increase size of points on the line

plot "dev_seq_projection_filter_by_count.dat" using 1:3:xtic(2) title "Simple projection", \
"dev_seq_projection_filter_by_count_inkeywords_substring.dat" using 1:3 title "In keywords (substring)", \
"dev_seq_projection_filter_by_count_inkeywords_exact.dat" using 1:3 title "In keywords (exact)"
