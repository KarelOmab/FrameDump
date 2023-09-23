
# Framedump

A simple Python script that extracts frames from a video and generates a sprite-image grid using ffmpeg and ImageMagick.

## Prerequisites

-   Python 3.x
-   ffmpeg (Ensure it's accessible from the system's PATH)
-   ImageMagick (Ensure it's accessible from the system's PATH)

## Usage

    python3 framedump.py <video_source_path> <interval> <output_dir> <frame_height_px> <sprite_image_format>

Arguments:

-   `video_source_path`: Path to the source video file.
-   `interval`: Interval (in seconds) at which frames are extracted from the video.
-   `output_dir`: Directory where the extracted frames and the sprite-image grid will be saved.
-   `frame_height_px`: Height of each extracted frame in pixels. The width is determined automatically to maintain the aspect ratio.
-   `sprite_image_format`: The format for the sprite-image grid. Supported formats: `png`, `webp`.

Example:

    python3 framedump.py /path/to/video.mp4 1 /path/to/output 60 png

This will extract frames from `/path/to/video.mp4` every second, resize each frame to a height of 60 pixels (width adjusted to maintain aspect ratio), and generate a sprite-image grid in `png` format inside `/path/to/output`.

## How It Works

1.  Validates the provided command line arguments.
2.  Extracts frames from the video at the specified interval using ffmpeg.
3.  Creates a sprite-image grid from the extracted frames using ImageMagick.
4.  Cleans up and deletes the individual frames, leaving only the sprite-image grid in the output directory.

## Configuration

Several constants are set at the top of the script for easy customization, including:

-   `DIR_FRAMES`: The sub-directory inside `output_dir` where individual frames will be saved.
-   `DIR_SPRITES`: The sub-directory inside `output_dir` where the sprite-image grid will be saved.
-   `MAGICK_MAX_ROWS` and `MAGICK_MAX_COLS`: Max number of rows and columns for the sprite-image grid.
-   `KEEP_FRAME_DUMP`: Whether to keep the individual frames in the output directory after generating the sprite-image grid.