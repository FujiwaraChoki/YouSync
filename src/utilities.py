import os
import uuid

from datetime import datetime
from termcolor import colored

def print_ascii_art():
    """
    Print the ASCII art.

    :return: None
    """
    with open("assets/ascii_art.txt", "r") as ascii_art_file:
        print(colored(ascii_art_file.read(), 'red'))

def print_info(version):
    """
    Print the info message.

    :param version: The version.
    """
    print("\033[1;31mYouSync\033[0m  -  Unlimited File Storage with YouTube")
    print("\033[1;31mVersion\033[0m  -  " + version)
    print("\033[1;31mAuthor\033[0m   -  github.com/FujiwaraChoki")
    print("\033[1;31mLicense\033[0m  -  MIT")

def print_help():
    """
    Print the help message.

    :return: None
    """
    print("\n\nUsage: yousync [OPTION]... [FILE]...")
    print("Unlimited File Storage Solution using YouTube\n")
    print("  -h, --help\t\t\tPrint this help message and exit")
    print("  -v, --version\t\t\tPrint version information and exit")
    print("  -u, --upload\t\t\tUpload a file to Storage")
    print("  -d, --download\t\tDownload a file from Storage")
    print("  -l, --list\t\t\tList all files uploaded to Storage")
    print("  -ra, --remove-all\t\tRemove all files from Storage")
    print("  -r, --remove\t\t\tRemove a file from Storage")
    print("  -s, --search\t\t\tSearch for a file")
    print("  -mv, --move\t\t\tRename a file\n")
    print("Report bugs to: www.github.com/FujiwaraChoki/yousync/issues")

def file_exists(file_path):
    """
    Check if a file exists.

    :param file_path: The file path.

    :return: True if the file exists, False otherwise.
    """
    return os.path.exists(file_path)

def generate_temp_file_path():
    """
    Generate a temporary file path.

    :return: The temporary file path.
    """
    return "tmp/" + str(uuid.uuid4())

def parse_date(date):
    """
    Parse a date string to a datetime object and return the date in the format 'Y-m-d'.

    :param date: The date string.

    :return: The parsed date string in 'Y-m-d' format.
    """
    parsed_date = datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S.%f")
    return colored(parsed_date.strftime("%d-%m-%Y"), "light_blue")
