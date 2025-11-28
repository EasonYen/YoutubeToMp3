import shutil
import sys
import os

def check_ffmpeg_installed():
    """
    Check if FFmpeg is installed and available in the system PATH.
    Returns the path to ffmpeg if installed, None otherwise.
    """
    path_in_env = shutil.which("ffmpeg")
    if path_in_env is not None:
        return path_in_env

    # Common paths for macOS/Linux where ffmpeg might be installed but not in PATH for GUI apps
    common_paths = [
        "/opt/homebrew/bin/ffmpeg",  # macOS Apple Silicon
        "/usr/local/bin/ffmpeg",     # macOS Intel
        "/usr/bin/ffmpeg",
        "/bin/ffmpeg"
    ]

    for path in common_paths:
        if os.path.isfile(path) and os.access(path, os.X_OK):
            # Found it! Add the directory to PATH so yt-dlp can find it too
            ffmpeg_dir = os.path.dirname(path)
            os.environ["PATH"] += os.pathsep + ffmpeg_dir
            print(f"Found ffmpeg at {path}, added to PATH")
            return path

    return None

def get_ffmpeg_install_guide():
    """
    Returns a dictionary containing installation guide URLs or instructions
    based on the operating system.
    """
    if sys.platform.startswith("win"):
        return {
            "os": "Windows",
            "url": "https://ffmpeg.org/download.html#build-windows",
            "command": "winget install FFmpeg"
        }
    elif sys.platform.startswith("darwin"):
        return {
            "os": "macOS",
            "url": "https://ffmpeg.org/download.html#build-mac",
            "command": "brew install ffmpeg"
        }
    elif sys.platform.startswith("linux"):
        return {
            "os": "Linux",
            "url": "https://ffmpeg.org/download.html#build-linux",
            "command": "sudo apt install ffmpeg"
        }
    else:
        return {
            "os": "Unknown",
            "url": "https://ffmpeg.org/download.html",
            "command": "Please install FFmpeg manually."
        }
