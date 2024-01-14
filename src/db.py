import os
import sys
import uuid
import sqlite3

from config import *
from datetime import datetime
from termcolor import colored
from pymongo import MongoClient
from utilities import parse_date
from prettytable import PrettyTable

# Define Variables
DB_PROVIDER = get_db_provider()
SQLITE_FILE_LOCATION = get_sqlite_file_location()
MONGODB_DB_NAME = get_mongodb_db_name()
VERBOSE = get_verbose()

def connect_mongodb():
    return MongoClient(get_mongo_uri())[MONGODB_DB_NAME]["files"]

def connect_sqlite():
    conn = sqlite3.connect(SQLITE_FILE_LOCATION)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS files
                (id text, file_path text, video_path text)""")
    return conn, cursor

def init_db():
    """
    Initialize the database.

    :return: None    
    """
    if VERBOSE:
            print(colored("\n\n[+] Initializing database...", "light_cyan"))

    if DB_PROVIDER == "mongodb":
        files_collection = connect_mongodb()
        if VERBOSE:
            print(colored("[+] Database initialized successfully\n", "light_green"))
        return files_collection
    elif DB_PROVIDER == "sqlite":
        conn, cursor = connect_sqlite()
        conn.commit()
        conn.close()
        if VERBOSE:
            print(colored("[+] Database initialized successfully\n", "light_green"))
    else:
        raise Exception("Invalid database provider.")

def upload_file_connection(file_path, video_url, hash_id=None):
    """
    Upload a file connection to the database.

    :param file_path: The file path.
    :param video_url: The video URL.
    :param hash_id: The UUID string.

    :return: None
    """
    if DB_PROVIDER == "mongodb":
        files_collection = connect_mongodb()
        files_collection.insert_one({
            "id": str(uuid.uuid4() if hash_id is None else hash_id),
            "file_path": file_path,
            "video_path": video_url,
            "created_at": datetime.now()
        })
    elif DB_PROVIDER == "sqlite":
        conn, cursor = connect_sqlite()
        cursor.execute("INSERT INTO files VALUES (?, ?, ?)", (str(uuid.uuid4() if hash_id is None else hash_id), file_path, video_url))
        conn.commit()
        conn.close()
    else:
        raise Exception("Invalid database provider.")

def get_file(file_path):
    """
    Get a file from the database.

    :param file_path: The file path.

    :return: The file.
    """
    if DB_PROVIDER == "mongodb":
        files_collection = connect_mongodb()
        result = files_collection.find_one({"file_path": file_path})
        return result["video_path"] if result is not None else None
    elif DB_PROVIDER == "sqlite":
        conn, cursor = connect_sqlite()
        cursor.execute("SELECT * FROM files WHERE file_path=?", (file_path,))
        result = cursor.fetchone()
        conn.commit()
        conn.close()
        return result[2] if result is not None else None
    else:
        raise Exception("Invalid database provider.")
def get_video_for_file(file_path):
    """
    Get the video path for a file path.

    :param file_path: The file path.

    :return: The video path.
    """
    if DB_PROVIDER == "mongodb":
        files_collection = connect_mongodb()
        return files_collection.find_one({"file_path": file_path})["video_path"]
    elif DB_PROVIDER == "sqlite":
        conn, cursor = connect_sqlite()
        cursor.execute("SELECT * FROM files WHERE file_path=?", (file_path,))

        result = cursor.fetchone()

        conn.commit()
        conn.close()

        return result[2] if result is not None else None
    else:
        raise Exception("Invalid database provider.")


def get_file_for_video(video_path):
    """
    Get the file path for a video path.

    :param video_path: The video path.

    :return: The file path.
    """
    if DB_PROVIDER == "mongodb":
        files_collection = connect_mongodb()
        return files_collection.find_one({"video_path": video_path})["file_path"]
    elif DB_PROVIDER == "sqlite":
        conn, cursor = connect_sqlite()
        cursor.execute("SELECT * FROM files WHERE video_path=?", (video_path,))

        result = cursor.fetchone()

        conn.commit()
        conn.close()

        return result[1] if result is not None else None
    else:
        raise Exception("Invalid database provider.")

def get_video_for_file_by_hash(hash_id):
    """
    Get the video path for a file path using the file hash.

    :param hash_id: The UUID string.

    :return: The video path.
    """
    if DB_PROVIDER == "mongodb":
        files_collection = connect_mongodb()
        return files_collection.find_one({"id": hash_id})["video_path"]
    elif DB_PROVIDER == "sqlite":
        conn, cursor = connect_sqlite()
        cursor.execute("SELECT * FROM files WHERE id=?", (hash_id,))

        result = cursor.fetchone()

        conn.commit()
        conn.close()

        return result[2] if result is not None else None
    else:
        raise Exception("Invalid database provider.")

def remove_file_connection(file_path, video_path=None):
    """
    Remove a file connection from the database.

    :param file_path: The file path.
    :param video_path: The video path.

    :return: None
    """
    if DB_PROVIDER == "mongodb":
        files_collection = connect_mongodb()
        files_collection.delete_one({"file_path": file_path})
    elif DB_PROVIDER == "sqlite":
        conn, cursor = connect_sqlite()
        if video_path is None:
            cursor.execute("DELETE FROM files WHERE file_path=?", (file_path,))
        else:
            cursor.execute("DELETE FROM files WHERE video_path=?", (video_path,))

        conn.commit()
        conn.close()
    else:
        raise Exception("Invalid database provider.")

def list_files():
    """
    List all files in the database.

    :return: None
    """
    if DB_PROVIDER == "mongodb":
        files_collection = connect_mongodb()
        result = files_collection.find({})

        if not result:
            print(colored("[!] No files found", "yellow"))
            sys.exit(0)
        else:
            result = list(result)
    elif DB_PROVIDER == "sqlite":
        conn, cursor = connect_sqlite()
        cursor.execute("SELECT * FROM files")

        result = cursor.fetchall()

        conn.commit()
        conn.close()

    table = PrettyTable()

    table.field_names = ["📌 Index", "🔑 Hash", "📁 File Path", "🎬 YouTube URL", "📅 Created At"]

    for file in result:
        index = result.index(file) + 1
        if DB_PROVIDER == "mongodb":
            table.add_row([index, colored(file["id"], "light_cyan"), colored(file["file_path"], "light_magenta"), \
                            colored(file["video_path"], "light_yellow"), parse_date(file["created_at"])])
        elif DB_PROVIDER == "sqlite":
            table.add_row([index, colored(file[0], "light_cyan"), colored(file[1], "light_magenta"), \
                            colored(file[2], "light_yellow"), parse_date(file[3])])
        else:
            raise Exception("Invalid database provider.")
    print()
    print(table)


def remove_all_files():
    """
    Remove all files from the database.

    :return: None
    """
    if DB_PROVIDER == "mongodb":
        files_collection = connect_mongodb()
        files_collection.delete_many({})
    elif DB_PROVIDER == "sqlite":
        conn, cursor = connect_sqlite()
        cursor.execute("DELETE FROM files")

        conn.commit()
        conn.close()

    # Remove every file in the tmp directory
    for file in os.listdir("tmp"):
        os.remove("tmp/" + file)

    return True

def rename_file(file_path, new_file_path):
    """
    Rename a file in the database.

    :param file_path: The file path.
    :param new_file_path: The new file path.

    :return: None
    """
    if DB_PROVIDER == "mongodb":
        files_collection = connect_mongodb()
        
        # Try to find the file by file path, if null, find by hash
        result = files_collection.find_one({"file_path": file_path})
        if result is None:
            result = files_collection.find_one({"id": file_path})

        files_collection.update_one({"id": result["id"]}, {"$set": {"file_path": new_file_path}})
    elif DB_PROVIDER == "sqlite":
        conn, cursor = connect_sqlite()

        # Try to find the file by file path, if null, find by hash
        cursor.execute("SELECT * FROM files WHERE file_path=?", (file_path,))

        result = cursor.fetchone()

        if result is None:
            cursor.execute("SELECT * FROM files WHERE id=?", (file_path,))

            result = cursor.fetchone()

        cursor.execute("UPDATE files SET file_path=? WHERE id=?", (new_file_path, result[0]))

        conn.commit()
        conn.close()
    else:
        raise Exception("Invalid database provider.")


def search_files(query):
    """
    Search for files in the database.

    :param query: The search query (can be a file path or file ID).

    :return: None
    """
    file_id = None

    try:
        # Try to convert query to UUID
        file_id = str(uuid.UUID(query))
    except ValueError:
        # Query is not a valid UUID, continue with regular search
        pass

    if file_id:
        # Search by file ID
        if DB_PROVIDER == "mongodb":
            files_collection = connect_mongodb()
            result = files_collection.find_one({"id": file_id})
            if not result:
                print(colored("[!] No file found with ID: {}".format(file_id), "yellow"))
                sys.exit(0)
            else:
                result = [result]
        elif DB_PROVIDER == "sqlite":
            conn, cursor = connect_sqlite()
            cursor.execute("SELECT * FROM files WHERE id=?", (file_id,))
            result = cursor.fetchall()
            conn.commit()
            conn.close()
        else:
            raise Exception("Invalid database provider.")
    else:
        # Search by regular query
        if DB_PROVIDER == "mongodb":
            files_collection = connect_mongodb()
            result = files_collection.find({"file_path": {"$regex": query}})
            if not result:
                print(colored("[!] No files found", "yellow"))
                sys.exit(0)
            else:
                result = list(result)
        elif DB_PROVIDER == "sqlite":
            conn, cursor = connect_sqlite()
            cursor.execute("SELECT * FROM files WHERE file_path LIKE ?", ("%" + query + "%",))
            result = cursor.fetchall()
            conn.commit()
            conn.close()
        else:
            raise Exception("Invalid database provider.")

    table = PrettyTable()

    table.field_names = ["📌 Index", "🔑 Hash", "📁 File Path", "🎬 YouTube URL"]

    for file in result:
        index = result.index(file) + 1
        if DB_PROVIDER == "mongodb":
            table.add_row([index, file["id"], colored(file["file_path"], "light_magenta"), file["video_path"]])
        elif DB_PROVIDER == "sqlite":
            table.add_row([index, file[0], colored(file[1], "light_magenta"), file[2]])
        else:
            raise Exception("Invalid database provider.")

    print()
    print(table)
