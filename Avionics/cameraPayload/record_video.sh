#!/bin/bash

base=payload-video
if [[ -e $base.h264 ]] ; then
	i=0
	while [[ -e $base-$i.h264 ]] ; do
		let i++
	done
	base=$base-$i
fi
filename=$base.h264
duration_minutes=60
duration_millis=$(expr $duration_minutes \* 60 \* 1000)

echo "The video will be called: $filename and run for $duration_minutes minutes, or $duration_millis millis."
raspivid --nopreview -t $duration_millis -w 1280 -h 1024 -fps 30 -o $filename
