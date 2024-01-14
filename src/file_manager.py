from termcolor import colored
from config import get_verbose
from file2video import convert_file_to_video
from video2file import convert_video_to_file
from utilities import generate_temp_file_path

VERBOSE = get_verbose()

def convert_file(file_path, mode="encode"):
    """
    Convert a file to a video or it's original format using `file2video` and `video2file`.

    :param file_path: The file path.
    :param mode: The mode to use. Either `encode` or `decode`.

    :return: The file path of the converted file.
    """
    if VERBOSE:
            print(colored(f"[+] Converting {file_path if mode == 'encode' else file_path} to {'video' if mode == 'encode' else 'original file'}...", "light_cyan"))
    video_path = generate_temp_file_path() 


    if mode == "encode":
        convert_file_to_video(file_path, video_path + ".mp4")
    elif mode == "decode":
        convert_video_to_file(file_path, "tmp")
    
    if VERBOSE:
            print(colored(f"[+] Converted to video successfully: {video_path}.mp4", "light_green"))

    return video_path
