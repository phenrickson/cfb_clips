import yt_dlp
import os
import subprocess
import sys

# download videos at defined start and stop times
def download_video_segment(url, output_directory, start_time=None, end_time=None):
    """Download a specific segment from a YouTube video."""
    os.makedirs(output_directory, exist_ok=True)

    # Prepare FFmpeg arguments for start and end times if provided
    external_downloader_args = []
    if start_time:
        external_downloader_args += ['-ss', start_time]
    if end_time:
        external_downloader_args += ['-to', end_time]

    # Set up download options
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',  # Best video and audio, or best overall
        'outtmpl': os.path.join(output_directory, '%(title)s.%(ext)s'),  # Output template
        'merge_output_format': 'mp4',  # Merge to mp4 format
        'external_downloader': 'ffmpeg',
        'external_downloader_args': external_downloader_args,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# convert video to gif
def convert_to_gif(input_file, output_directory):
    """Convert a video file to GIF format using Gifski."""
    # Get the base name of the input file (without extension)
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = os.path.join(output_directory, f"{base_name}.gif")
    frames_dir = os.path.join(output_directory, f"{base_name}_frames")

    # Create a directory to store extracted frames
    os.makedirs(frames_dir, exist_ok=True)

    # Step 1: Extract frames with FFmpeg, resizing to a specific width (640 here)
    frame_pattern = os.path.join(frames_dir, "frame%04d.png")
    command_ffmpeg = [
        'ffmpeg',
        '-i', input_file,
        '-vf', 'fps=60,scale=640:-1',   # Adjust frame rate and resolution
        frame_pattern
    ]
    subprocess.run(command_ffmpeg)

    # Step 2: Convert frames to GIF using Gifski
    command_gifski = [
        'gifski', '--fps', '60', '-o', output_file
    ] + [os.path.join(frames_dir, f) for f in sorted(os.listdir(frames_dir))]
    
    # Execute the command to create the GIF
    subprocess.run(command_gifski)

    # Clean up frames directory after creating the GIF
    for file_name in os.listdir(frames_dir):
        os.remove(os.path.join(frames_dir, file_name))
    os.rmdir(frames_dir)
    
# function to read in videos from txt
def read_video_segments(file_path):
    video_segments = []
    # Read video segments from the specified text file
    with open(file_path, 'r') as file:
        for line in file:
            # Strip whitespace and split by spaces
            parts = line.strip().split()
            if len(parts) == 3:  # Check if the line contains exactly 3 parts
                url, start, end = parts  # Unpack the URL, start time, and end time
                video_segments.append({'url': url, 'start': start, 'end': end})  # Append the segment as a dictionary

    return video_segments
