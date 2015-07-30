set title "vidoe-short.json"
set xlabel "time (s)"
set ylabel "power (mJ)"
set terminal pdf
set output "video-short-acc.pdf"
plot "video-short-performance.data" u 1:4 w l t "performance", "video-short-ondemand.data" u 1:4 w l t "ondemand", "video-short-sched.data" u 1:4 w l t "sched", "video-short-conservative.data" u 1:4 w l t "conservative", "video-short-powersave.data" u 1:4 w l t "powersave"
