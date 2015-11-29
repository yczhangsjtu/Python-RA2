name=$1
filename=$1.png
X=$2
Y=$3
W=$4
H=$5
w=$6
h=$7
I=$8
J=$9


for i in `seq 0 1 $(($I-1))`; do
	x=$(($i*$W+$X))
	convert -crop ${w}x0+$x+0 $filename "tmp_${i}.png"
	l="$l tmp_${i}.png"
done
convert +append $l tmp1.png
rm $l

l=""
for j in `seq 0 1 $(($J-1))`; do
	y=$(($j*$H+$Y))
	convert -crop 0x${h}+0+$y tmp1.png "tmp_${j}.png"
	l="$l tmp_${j}.png"
done
convert -append $l output.png 
rm $l tmp1.png
