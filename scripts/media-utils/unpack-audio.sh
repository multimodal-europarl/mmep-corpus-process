#!/bin/bash

U="_"
file_path=$1
file_base=$2
echo $file_path
echo $file_base
ffmpeg -i $file_path/$file_base.mp4 2>&1 | grep "Stream #" | while read -r line ; do
    echo $line
    iso=$(echo $line | grep -oP '(?<=\().{3}(?=\))') #[0-9]\(\K[^\)]+')
    stream=$(echo $line | grep -oP '0:[0-9]{1,2}')
    stream2=${stream:2}
    if [ "$stream" == "0:1" ] || [ "$iso" != "und" ] ; then
        echo "  $iso  -  $stream  -  $stream2"
        ffmpeg -loglevel error -nostdin -i $file_path/$file_base.mp4 -map $stream $file_path/$U$stream2$U$iso$U$file_base.wav
        #ffmpeg -loglevel fatal -hide_banner -nostdin -i $1/$file_base/$file -map $stream $1/$file_base/$U$stream2$U$iso$U$file_base.mp3
    fi
done
