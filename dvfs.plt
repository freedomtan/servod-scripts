set title "vidoe-short.json"
set xlabel "time (s)"
set ylabel "power (mJ)"
set terminal pdf
set output "video-short.pdf"
plot "video-short-performance.data" w l t "performance", "video-short-ondemand.data" w l t "ondemand", "video-short-sched.data" w l t "sched", "video-short-conservative.data" w l t "conservative", "video-short-powersave.data" w l t "powersave"
