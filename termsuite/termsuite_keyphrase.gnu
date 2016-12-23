reset # do not use any previous settings
set title "Termsuite - Keyphrase extraction" # chart title
set xlabel "wrlog filter" # x-axis label
set ylabel "Precision/Recall/f1-score" # y-axis label
set term png size 800, 400
set size ratio 0.4
set output "termsuite.png" # name of image file (change to .eps for eps file)
set xtics 2.0, 0.2, 6.0  # set increment for x-axis
set ytics 0.1 
set key left top
set style data linespoints # set default way of data plotting
set pointsize 1.5 # increase size of points on the line

plot "termsuite_ann.dat" using 1:2 title "precision", \
"termsuite_ann.dat" using 1:3 title "recall", \
"termsuite_ann.dat" using 1:4 title "f1-score"
