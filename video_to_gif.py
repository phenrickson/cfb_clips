# video_to_gif.py
import os
from functions import download_video_segment, convert_to_gif, read_video_segments

# Define the output directories
video_directory = 'downloaded_segments'
gif_directory = 'gifs'

# Create output directories
os.makedirs(video_directory, exist_ok=True)
os.makedirs(gif_directory, exist_ok=True)

# Read video segments from a text file
video_segments = read_video_segments('videos.txt')

# Loop through the list of URLs, download each segment, and convert to GIF
for segment in video_segments:
    print(f'Downloading segment from: {segment["url"]} (from {segment["start"]} to {segment["end"]})')
    video_filename = download_video_segment(segment['url'], video_directory, segment['start'], segment['end'])
    print('Download complete!\n')

# Loop through all MP4 files in the input directory
for file_name in os.listdir(video_directory):
    if file_name.endswith('.mp4'):  # Process only MP4 files
        input_file_path = os.path.join(video_directory, file_name)
        print(f'Converting {input_file_path} to GIF using Gifski...')
        convert_to_gif(input_file_path, gif_directory)
        print(f'Conversion complete! Saved to {gif_directory}\n')
