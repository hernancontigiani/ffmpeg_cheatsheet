# FFmpeg cheatsheet
FFmpeg cheatsheet for crop, contact videos, create gifs and video modification

# Crop videos
Crop a input video (in.mp4) from a specific start time (-ss MM:SS):
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

# Concact videos of different resolutions or codec
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
