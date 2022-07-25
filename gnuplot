set xdata time

set datafile separator ";"
set format x "%S"
set grid xtics
plot "front-rotor-run-1.csv" u ($1/1000):2 w linespoints

