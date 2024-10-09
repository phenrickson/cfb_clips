import os
import sys
from functions import download_video_segment, convert_to_gif, read_video_segments

# Define the output directories
video_directory = 'downloaded_segments'
gif_directory = 'gifs'
processed_file = 'processed_videos.txt'  # File to track processed GIFs

# Create output directories
os.makedirs(video_directory, exist_ok=True)
os.makedirs(gif_directory, exist_ok=True)

def process_videos(video_segments):
    processed_videos = set()

    # Read processed videos from the processed file
    if os.path.exists(processed_file):
        with open(processed_file, 'r') as f:
            processed_videos = set(line.strip() for line in f)

    for segment in video_segments:
        # Create a unique output GIF name
        output_gif = os.path.join(gif_directory, f"{segment['url'].split('=')[-1]}_{segment['start'].replace(':', '')}_{segment['end'].replace(':', '')}.gif")
        
        # Check if this GIF has already been processed
        if output_gif in processed_videos:
            print(f"Skipping already processed segment: {segment['url']} (from {segment['start']} to {segment['end']})")
            continue
        
        # Download and convert if not processed
        print(f'Downloading segment from: {segment["url"]} (from {segment["start"]} to {segment["end"]})')
        video_filename = download_video_segment(segment['url'], video_directory, segment['start'], segment['end'])
        print('Download complete!\n')

        # Convert to GIF
        print(f'Converting {video_filename} to GIF using Gifski...')
        convert_to_gif(video_filename, gif_directory)
        print(f'Conversion complete! Saved to {gif_directory}\n')

        # Mark this GIF as processed
        processed_videos.add(output_gif)

    # Save the processed video names back to the file
    with open(processed_file, 'w') as f:
        for video in processed_videos:
            f.write(f"{video}\n")

# Read video segments from a text file
video_segments = read_video_segments('videos.txt')

# Process videos
process_videos(video_segments)