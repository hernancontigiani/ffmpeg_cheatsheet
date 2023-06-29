# FFmpeg cheatsheet
FFmpeg cheatsheet for crop, contact videos, create gifs and video modification

## Crop videos
Crop a input video (in.mp4) from a specific start stamp (-ss MM:SS):
```sh
$ ffmpeg -ss 0:10 -i in.mp4 -c copy out.mp4 -y
```
Crop a input video (in.mp4) to a specific duration time (-t MM:SS):
```sh
$ ffmpeg -t 1:40 -i in.mp4 -c copy out.mp4 -y
```
Crop a input video (in.mp4) from time seconds 10 to time seconds 30 (duration 20 seconds):
```sh
$ ffmpeg -ss 0:10 -t 0:20 -i in.mp4 -c copy out.mp4 -y
```

## Concat videos from same source (same video resolution, codec and FPS)
In case you have crop a video into multiple subvideos, use this command to concat them again:
```sh
$ ffmpeg -f concat -safe 0 -i tramo_list.txt -c copy out.mp4 -y
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
$ ffmpeg -i in1.mp4 -i in2.mp4 -filter_complex \
"[0:v] [0:a] [1:v] [1:a] concat=n=2:v=1:a=1 [v][a]" \
-map "[v]" -map "[a]" -c:v libx264 -c:a aac -movflags +faststart out.mp4
```

In case they dont share the same resolution, concat two videos using first video resolution (1280x780, adapt this to your video) and change second video to adapt to that resolution:
```sh
$ ffmpeg -i in1.mp4 -i in2.mp4 -filter_complex \
"[0:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2[v0]; \
 [v0][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]" \
-map "[v]" -map "[a]" -c:v libx264 -c:a aac -movflags +faststart out.mp4
```

## Transform video codec
From MP4 (mpeg) to H264:
```sh
$ ffmpeg -i int.mp4 -c:v libx264 out.h264 -y
```
From MP4/H264 to High profile (level 4):
```sh
$ ffmpeg -i in.mp4 -c:v libx264 -profile:v high -level:v 4.0 -pix_fmt yuv420p -c:a copy out.h264 -y
```

From MP4 to H265
```sh
$ ffmpeg -i input.mp4 -c:v libx265 -vtag hvc1 out.mp4
```
## Change video speed
Duplicate speed (speed up):
```
$ ffmpeg -i in.mp4 -filter:v "setpts=0.5*PTS" out.mp4
```
Half speed (speed down):
```
$ ffmpeg -i in.mp4 -filter:v "setpts=2*PTS" out.mp4
```

## Change video FPS without change speed
Example of how to change FPS to 10
```sh
$ ffmpeg -i in.mp4 -filter:v fps=fps=10 out.mp4
```

## Create a image frame from a video
Get a image from FRAME nº10:
```sh
$ sudo ffmpeg -ss 10 -i in.mp4 -vframes 1 -f image2 out.jpg
```

## Create a video from a static image
Create a h264 video from input image, of 15 seconds duration:
```sh
$ ffmpeg -loop 1 -i int.jpg -t 15 out.h264
```

## Create a gif from video
Create a gif from in.mp4 video from start stamp 3s of 7seconds duration
```sh
$ ffmpeg -ss 0:03 -t 0:07 -i in.mp4 -vf "fps=10,scale=720:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 out.gif
```

# Play webcam video
Use "video0" for notebook camera, use "video1" for USB webcam
```
$ ffplay /dev/video0
```

# Record webcam video
Use "video0" for notebook camera, use "video1" for USB webcam
```
$ ffmpeg -f v4l2 -framerate 20 -video_size 1280x720 -input_format mjpeg -i /dev/video0 out.mp4 -y
```

# Add a overlay image
In this example we are adding a overlay image in top-left corner (0,0) in the first 8 seconds (from 0 to 8). If the image is bigger than the video original resolution it will be cut.
```
ffmpeg -i in.mp4 -i image.jpg -filter_complex "[0:v][1:v] overlay=0:0:enable='between(t,0,8)'" -pix_fmt yuv420p -c:a copy out.mp4
```


