import sys

from db import *
from files import *
from utilities import *

VERSION = "1.0.2"


def main():
    # Print ASCII art
    print_ascii_art()

    # Print info
    print_info(VERSION)

    # Prepare output/working directories
    prepare_directories()

    # Initialize the database
    init_db()

    argc = len(sys.argv)

    i = 1
    while i < argc:
        if sys.argv[i].startswith(("-h", "--help")):
            print_help()
            sys.exit(0)
        elif sys.argv[i].startswith(("-v", "--version")):
            print(colored(f"\nYouSync is currently on version {VERSION}", "light_blue"))
            sys.exit(0)
        elif sys.argv[i].startswith(("-s", "--search")):
            if i + 1 < argc:
                query = sys.argv[-1]

                search_files(query)
            else:
                print("\n\nMissing argument after", sys.argv[i])
                sys.exit(1)
            i += 2
        elif sys.argv[i].startswith(("-u", "--upload")):
            if i + 1 < argc:
                path = sys.argv[-1]

                if file_exists(path):
                    if upload_file(path):
                        print(
                            "\033[1;32m\n[+] File upload successful:", path, "\033[0m"
                        )
                    else:
                        print("\033[1;33m\n\nFile upload failed:", path, "\033[0m")
                else:
                    print("\n\nFile does not exist:", path)
                    sys.exit(1)
            else:
                print("\n\nMissing argument after", sys.argv[i])
                sys.exit(1)
            i += 2
        elif sys.argv[i].startswith(("-d", "--download")):
            if i + 1 < argc:
                path = sys.argv[-1]

                result = download_file(path)

                if result:
                    print(
                        "\033[1;32m\n[+] File download successful:", result, "\033[0m"
                    )
                else:
                    print("\033[1;33m\n\nFile download failed:", path, "\033[0m")

            else:
                print("\n\nMissing argument after", sys.argv[i])
                sys.exit(1)
            i += 2
        elif sys.argv[i] == ("-r", "--remove"):
            if i + 1 < argc:
                path = sys.argv[-1]

                if file_exists(path):
                    if remove_file(path):
                        print(
                            "\033[1;32m\n[+] File remove successful:", path, "\033[0m"
                        )
                    else:
                        print("\033[1;33m\nFile remove failed:", path, "\033[0m")
                else:
                    print("\nFile does not exist:", path)
                    sys.exit(1)
            else:
                print("\nMissing argument after", sys.argv[i])
                sys.exit(1)
            i += 2
        elif sys.argv[i].startswith(("-mv", "--move-file")):  # Also means rename
            if i + 2 < argc:
                path = sys.argv[-2]
                new_path = sys.argv[-1]

                if file_exists(path):
                    if rename_file(path, new_path):
                        print(
                            "\033[1;32m\n[+] File rename successful:",
                            path,
                            "->",
                            new_path,
                            "\033[0m",
                        )
                    else:
                        print(
                            "\033[1;33m\n\nFile rename failed:",
                            path,
                            "->",
                            new_path,
                            "\033[0m",
                        )
                else:
                    print("\n\nFile does not exist:", path)
                    sys.exit(1)
            else:
                print("\n\nMissing argument after", sys.argv[i])
                sys.exit(1)
            i += 3

        elif sys.argv[i].startswith(("-ra", "--remove-all")):
            if remove_all_files():
                print("\033[1;32m\n[+] All files removed successfully\033[0m")
            else:
                print("\033[1;33m\n\nFailed to remove all files\033[0m")
            i += 1
        elif sys.argv[i].startswith(("-l", "--list")):
            list_files()
            sys.exit(0)
        else:
            print("\n\nInvalid argument:", sys.argv[i])
            print("Try 'yousync --help' for more information.")
            sys.exit(1)


if __name__ == "__main__":
    main()
