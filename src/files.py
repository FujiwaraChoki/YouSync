import os
import uuid

from yt import *
from db import *
from utilities import *
from file_manager import convert_file

def upload_file(file_path):
    # Create UUID
    hash_id = str(uuid.uuid4())

    # Convert the file to a video
    video_path = convert_file(file_path, mode="encode")

    # Upload file to YouTube
    video_url = upload_video(video_path + ".mp4", hash_id, file_path)

    if not video_url:
        return False

    # Save the file path and video path to the database
    print(colored(f"\n[+] Saving file to database...", "light_cyan"))
    absolute_file_path = os.path.abspath(file_path)
    upload_file_connection(absolute_file_path, video_url, hash_id=hash_id)
    print(colored(f"[+] Saved file to database successfully: {file_path}", "light_green"))

    return True

def download_file(file_path):
    # Get the video path for the file path
    result = get_file(file_path)

    if not result:
        if VERBOSE:
            print(colored("[!] Getting video for file failed. Trying by hash...", "blue"))
        result = get_video_for_file_by_hash(file_path)

    temp_path = generate_temp_file_path() + ".mp4"

    # Download YouTube video by url
    download_video(result, temp_path)

    return True

def remove_file(file_path):
    # Get the video path for the file path
    result = get_video_for_file(file_path)

    if not result:
        return False
    
    # Remove the video
    os.remove(result)

    # Remove the file from the database
    remove_file_connection(file_path)

    return True