# FFmpeg cheatsheet
FFmpeg cheatsheet for crop, contact videos, create gifs and video modification

## Crop videos
Crop a input video (in.mp4) from a specific start stamp (-ss MM:SS):
```sh
ffmpeg -ss 0:10 -i in.mp4 -c copy out.mp4 -y
```
Crop a input video (in.mp4) to a specific duration time (-t MM:SS):
```sh
ffmpeg -t 1:40 -i in.mp4 -c copy out.mp4 -y
```
Crop a input video (in.mp4) from time seconds 10 to time seconds 30 (duration 20 seconds):
```sh
ffmpeg -ss 0:10 -t 0:20 -i in.mp4 -c copy out.mp4 -y
```

## Concat videos from same source (same video resolution, codec and FPS)
In case you have crop a video into multiple subvideos, use this command to concat them again:
```sh
ffmpeg -f concat -safe 0 -i tramo_list.txt -c copy out.mp4 -y
```
In "tramo_list" it specify which videos concat:
```
file 'in1.mp4'
file 'in2.mp4'
file 'in3.mp4'
```

## Concact videos of different resolutions or codec
Reference:\
https://ottverse.com/3-easy-ways-to-concatenate-mp4-files-using-ffmpeg/

In they share the same resolution but diferent codec or FPS use:
```sh
ffmpeg -i in1.mp4 -i in2.mp4 -filter_complex \
"[0:v] [0:a] [1:v] [1:a] concat=n=2:v=1:a=1 [v][a]" \
-map "[v]" -map "[a]" -c:v libx264 -c:a aac -movflags +faststart out.mp4
```

In case they dont share the same resolution, concat two videos using first video resolution (1280x780, adapt this to your video) and change second video to adapt to that resolution:
```sh
ffmpeg -i in1.mp4 -i in2.mp4 -filter_complex \
"[0:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2[v0]; \
 [v0][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]" \
-map "[v]" -map "[a]" -c:v libx264 -c:a aac -movflags +faststart out.mp4
```

## Transform MP4 (mpeg) to H264
```sh
ffmpeg -i int.mp4 -c:v libx264 out.h264 -y
```

## Create a image frame from a video
Get a image from FRAME nº10:
```sh
sudo ffmpeg -ss 10 -i in.mp4 -vframes 1 -f image2 out.jpg
```

## Create a video from a static image
Create a h264 video from input image, of 15 seconds duration:
```sh
ffmpeg -loop 1 -i int.jpg -t 15 out.h264
```

## Create a gif from video
Create a gif from in.mp4 video from start stamp 3s of 7seconds duration
```sh
ffmpeg -ss 0:03 -t 0:07 -i in.mp4 -vf "fps=10,scale=720:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 out.gif
```

