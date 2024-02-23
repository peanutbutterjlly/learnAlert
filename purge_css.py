from pathlib import Path
import os

# Define base directory
base_dir = Path(__file__).resolve().parent.as_posix()

# Define CSS files
css_files = [
    f"{base_dir}/apps/main/static/styles.css",
    f"{base_dir}/apps/main/static/pico.css",
]

# Exclude venv directory
excluded_directory = f"{base_dir}/venv"

# Initialize list for HTML files
html_files = []

# Iterate through directory and subdirectories to find HTML files
for root, dirs, files in os.walk(base_dir):
    dirs[:] = [d for d in dirs if d != "venv"]  # Exclude venv directory
    for file in files:
        if file.endswith(".html"):
            absolute_path = f"{root}/{file}"
            html_files.append(absolute_path)

# Define output file
output_file = f"{base_dir}/static/build/"

# Print command for purging CSS
print(
    f"npx purgecss --css {' '.join(css_files)} --content {' '.join(html_files)} --output {output_file}"
)
