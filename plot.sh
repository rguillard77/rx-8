#!/usr/bin/gnuplot -c

set term qt persist
set xdata time

set datafile separator ";"
set format x "%S"
set grid xtics
plot ARG1 u ($1/1000):2  w linespoints
# u ($1/1000):2 w linespoints
