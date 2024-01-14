import os
import uuid

from termcolor import colored

def print_ascii_art():
    with open("assets/ascii_art.txt", "r") as ascii_art_file:
        print(colored(ascii_art_file.read(), 'red'))

def print_info(version):
    print("\033[1;31mYouSync\033[0m  -  Unlimited File Storage with YouTube")
    print("\033[1;31mVersion\033[0m  -  " + version)
    print("\033[1;31mAuthor\033[0m   -  github.com/FujiwaraChoki")
    print("\033[1;31mLicense\033[0m  -  MIT")

def print_help():
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
    print("  -mv, --move\t\t\tRename a file")
    print("Report bugs to: www.github.com/FujiwaraChoki/yousync/issues")

def file_exists(file_path):
    return os.path.exists(file_path)

def generate_temp_file_path():
    return "tmp/" + str(uuid.uuid4())

