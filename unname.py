import os
import re

# Directory containing the renamed files
directory = r'\\server\Plex\folder'

# Regex to capture filenames with the sYYYYeXXX pattern
pattern = re.compile(r'^(.*?)_s\d{4}e\d{3}_(.*)\.([a-zA-Z0-9]+)$')

# Process all files and revert the renaming
for filename in os.listdir(directory):
    if os.path.isfile(os.path.join(directory, filename)):
        match = pattern.match(filename)
        if match:
            original_prefix, rest_of_name, ext = match.groups()
            # Create the new filename by removing the sYYYYeXXX part
            original_filename = f"{original_prefix}_{rest_of_name}.{ext}"
            os.rename(os.path.join(directory, filename), os.path.join(directory, original_filename))