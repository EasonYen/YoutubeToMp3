import PyInstaller.__main__
import os
import sys

# Determine icon extension based on OS
icon_file = "icon.ico" if sys.platform.startswith("win") else "icon.png"

if not os.path.exists(icon_file):
    print(f"Error: {icon_file} not found. Please run create_icon.py first.")
    sys.exit(1)

print("Starting build process...")

PyInstaller.__main__.run([
    'src/main.py',
    '--name=YoutubeToMp3',
    '--onefile',
    '--windowed',  # No console window
    f'--icon={icon_file}',
    '--clean',
])

print("Build complete. Check the 'dist' folder.")
