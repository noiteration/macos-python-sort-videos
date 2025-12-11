import os
import subprocess
import shutil

# Directories
source_dir = "./"
landscape_dir = os.path.join(source_dir, "landscape")
portrait_dir = os.path.join(source_dir, "portrait")

# Create folders if they don't exist
os.makedirs(landscape_dir, exist_ok=True)
os.makedirs(portrait_dir, exist_ok=True)

def get_dimensions(file_path):
    """Return (width, height) using macOS mdls metadata."""
    try:
        cmd = ["mdls", "-name", "kMDItemPixelWidth", "-name", "kMDItemPixelHeight", file_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stdout

        width = None
        height = None
        for line in output.splitlines():
            if "kMDItemPixelWidth" in line:
                width = int(line.split('=')[1].strip())
            elif "kMDItemPixelHeight" in line:
                height = int(line.split('=')[1].strip())
        
        return width, height
    except Exception as e:
        print(f"Failed to get dimensions for {file_path}: {e}")
        return None, None

# Loop through videos
for file in os.listdir(source_dir):
    if file.lower().endswith(".mov"):
        file_path = os.path.join(source_dir, file)
        if not os.path.isfile(file_path):
            continue

        width, height = get_dimensions(file_path)
        if width is None or height is None:
            print(f"Skipping {file}, unable to get dimensions")
            continue

        # Decide folder based on width/height
        if width > height:
            dest_dir = landscape_dir
        elif height > width:
            dest_dir = portrait_dir
        else:
            print(f"Skipping square video: {file}")
            continue

        # Handle duplicate filenames
        dest_path = os.path.join(dest_dir, file)
        base, ext = os.path.splitext(file)
        counter = 1
        while os.path.exists(dest_path):
            dest_path = os.path.join(dest_dir, f"{base}_{counter}{ext}")
            counter += 1

        print(f"Moving {file_path} → {dest_path}")
        shutil.move(file_path, dest_path)
