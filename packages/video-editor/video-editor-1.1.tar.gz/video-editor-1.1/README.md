# Video Editor

Video editing tool using ffmpeg.
The tool has the ability to cut as many unnecessary video frames as specified in a YAML file.

## Dependencies
- ffmpeg

## Install
Use ```pip install video-editor``` to install.

## How To
1. Ensure the `ffmpeg` package is installed. Use `brew install ffmpeg` to install on MacOSX.
2. Create a YAML file with frames to either select or delete. 
Here is a sample YAML: ```myrecording.yaml```
```
---
input: "input-video.mp4"
output: "output-video.mp4"
cut_method: select  # use 'delete' to remove unwanted frames
timeframe:
  - from: start   # first frame
    to: 4m
  - from: 10m11s  # selected frames
    to: 15m50s
  - from: 30m5s   # selected frames
    to: end       # last frame
```
3. Execute the following command:
`video-cut -p myrecording.yaml`
where, `-p` is the YAML with editing instruction.
4. You should now get the `output-video.mp4` video file after the process is over.

## Future Enhancements
- Move from `ffmpeg` tool to `ffmpeg-python` library
- Add feature to screen grab based on screen coordinates 
