import os
import re
from datetime import datetime

# Directory containing the downloaded files
directory = r'\\server\Plex\folder'

# Get the current year (used as season number)
current_year = datetime.now().year

# Regex to capture filenames with existing sYYYYeXXX pattern
pattern = re.compile(r'_s\d{4}e(\d{3})_')

# Initialize episode counter to 1
episode_counter = 1

# First, find the highest episode number
for filename in os.listdir(directory):
    match = pattern.search(filename)
    if match:
        episode_num = int(match.group(1))
        episode_counter = max(episode_counter, episode_num + 1)

# Regex to capture the part before and after the first '_'
filename_pattern = re.compile(r'^(.*?)_(.*)\.([a-zA-Z0-9]+)$')

# Store files in pairs
file_pairs = {}

# First, group files (e.g., mkv and nfo) by common part
for filename in os.listdir(directory):
    if os.path.isfile(os.path.join(directory, filename)):
        match = filename_pattern.match(filename)
        if match:
            prefix, rest_of_name, ext = match.groups()
            base_name = f"{prefix}_{rest_of_name}"
            if base_name not in file_pairs:
                file_pairs[base_name] = []
            file_pairs[base_name].append((filename, ext))

# Process each pair of files
for base_name, files in file_pairs.items():
    # Only rename if no files in the pair already contain sYYYYeXXX
    if not any(pattern.search(f[0]) for f in files):
        for filename, ext in files:
            new_filename = f"{base_name.split('_')[0]}_s{current_year}e{episode_counter:03}_{base_name.split('_')[1]}.{ext}"
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))

        # Increment the episode counter after processing both the video and nfo file
        episode_counter += 1