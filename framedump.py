import sys
import os
import subprocess
import shutil

# Constants
DIR_FRAMES = 'frames'
DIR_SPRITES = 'sprites'
FFMPEG_FRAME_FORMAT = 'png'
MAGICK_MAX_ROWS = 60
MAGICK_MAX_COLS = 60
MAGICK_OUTPUT_PREFIX = 'sprite_image_grid'
KEEP_FRAME_DUMP = False

magick_accepted_formats = {'png', 'webp'}

# input validation functions
def is_valid_file_path(path):
    return os.path.isfile(path)

def is_suitable_directory_path(path):
    # Check if the path points to an existing file
    if os.path.isfile(path):
        print(f"output_dir error: '{path}' points to an existing file.")
        return False

    # Get the parent directory of the path
    parent_dir = os.path.dirname(path)

    # If the parent directory doesn't exist, the path isn't suitable
    if not os.path.exists(parent_dir):
        print(f"output_dir error: '{path}' the parent directory doesn't exist.")
        return False

    # Check if we have write permissions to the parent directory
    # (This step might be OS-dependent; the following check works on Unix-based systems.)
    if not os.access(parent_dir, os.W_OK):
        print(f"output_dir error: '{path}' no write permissions to the parent directory.")
        return False

    return True

def is_valid_sprite_image_format(format):
    return format in magick_accepted_formats

def validate_args(video_source_path, interval, output_dir, frame_height_px, sprite_image_format):
    if not is_valid_file_path(video_source_path):
        print(f"video_source_path error: '{video_source_path}' is not a valid file path.")
        return False

    if not (interval.isdigit() and int(interval) >= 1):
        print(f"interval error: '{interval}' is not a positive integer (expecting >= 1).")
        return False

    if not is_suitable_directory_path(output_dir):
        return False
    
    if not (frame_height_px.isdigit() and int(frame_height_px) >= 1):
        print(f"frame_height_px error: '{interval}' is not a positive integer (expecting >= 1).")
        return False

    if not is_valid_sprite_image_format(sprite_image_format):
        print(f"sprite_image_format error: '{sprite_image_format}' is not an accepted image format {magick_accepted_formats}.")
        return False

    return True

def extract_frames_using_ffmpeg(data):
    cmd = [
        'ffmpeg', 
        '-i', data['video_source_path'], 
        '-vf', f'fps=1/{data["interval"]},scale=-1:{data["frame_height_px"]}', 
        os.path.join(data['output_dir_frames'], f'frame%06d.{FFMPEG_FRAME_FORMAT}')
    ]
    
    subprocess.run(cmd, check=True)

def create_sprite_image_grid(data):
    # Get the list of images in the output_dir
    image_list = os.path.join(data['output_dir_frames'], f'*.{FFMPEG_FRAME_FORMAT}')
    
    # Form the montage command
    cmd = [
        'montage', 
        image_list,
        '-geometry', '+0+0', 
        '-tile', f'{MAGICK_MAX_COLS}x{MAGICK_MAX_ROWS}', 
        os.path.join(data['output_dir_sprites'], MAGICK_OUTPUT_PREFIX + '.' + data['sprite_image_format'])
    ]
    
    subprocess.run(cmd, check=True)

def main():
    d = {
        'video_source_path' : '/foo/bar/baz/bat.mp4',
        'interval' : '1',
        'output_dir' : '/foo/bar/baz/output',
        'frame_height_px' : '60',
        'sprite_image_format' : 'png'
    }

    if len(sys.argv) != 6:
        print("Incorrect amount of arguments!")
        print("Usage: {} {}".format('framedump.py', ' '.join(d.keys())))
        print("Example: {} {}".format('framedump.py', ' '.join(d.values())))
        sys.exit()
        

    video_source_path, interval, output_dir, frame_height_px, sprite_image_format = sys.argv[1:]

    if not validate_args(video_source_path, interval, output_dir, frame_height_px, sprite_image_format):
        sys.exit()

    # validation passed
    d['video_source_path'] = video_source_path
    d['interval'] = interval
    d['output_dir'] = output_dir
    d['frame_height_px'] = frame_height_px
    d['sprite_image_format'] = sprite_image_format
    d['output_dir_frames'] = os.path.join(output_dir, DIR_FRAMES)
    d['output_dir_sprites'] = os.path.join(output_dir, DIR_SPRITES)

    # After validation, start processing

    # 1. Check if the output_dir/frames directory exists, and if not, attempt to create it
    frame_dir = d['output_dir_frames']
    if not os.path.exists(frame_dir):
        try:
            os.makedirs(frame_dir)
            print(f"Directory '{d['output_dir']}' created successfully.")
        except OSError as e:
            print(f"Failed to create directory '{frame_dir}'. Error: {e}")
            sys.exit()

    sprite_dir = d['output_dir_sprites']
    if not os.path.exists(sprite_dir):
        try:
            os.makedirs(sprite_dir)
            print(f"Directory '{d['output_dir']}' created successfully.")
        except OSError as e:
            print(f"Failed to create directory '{sprite_dir}'. Error: {e}")
            sys.exit()

    # 2. Extract frames using ffmpeg
    try:
        extract_frames_using_ffmpeg(d)
        print("Frames extracted successfully!")
    except subprocess.CalledProcessError:
        print("Failed to extract frames. Please ensure ffmpeg is accessible and working.")

    # 3. Create sprite sheet
    try:
        create_sprite_image_grid(d)
        print("Sprite-image grid created successfully!")
    except subprocess.CalledProcessError:
        print("Failed to create sprite-image grid. Please ensure ImageMagick is accessible and working.")

    # 4. Cleanup?
    if not KEEP_FRAME_DUMP and os.path.exists(frame_dir):
        try:
            shutil.rmtree(frame_dir)
            print(f"Directory '{frame_dir}' deleted successfully.")
        except Exception as e:
            print(f"Failed to delete directory '{frame_dir}'. Error: {e}")
            

if __name__ == "__main__":
    main()