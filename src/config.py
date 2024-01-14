import json

def get_mongo_uri():
    """
    Get the Mongo URI.

    :return: The Mongo URI.
    """
    return json.loads(open("config.json", "r").read())["mongodb_uri"]

def get_db_provider():
    """
    Get the database provider.

    :return: The database provider.
    """
    return json.loads(open("config.json", "r").read())["db_provider"]

def get_sqlite_file_location():
    """
    Get the SQLite file location.

    :return: The SQLite file location.
    """
    return json.loads(open("config.json", "r").read())["sqlite_file_location"]

def get_mongodb_db_name():
    """
    Get the MongoDB database name.

    :return: The MongoDB database name.
    """
    return json.loads(open("config.json", "r").read())["mongodb_db_name"]

def get_firefox_profile_location():
    """
    Get the Firefox profile location.

    :return: The Firefox profile location.
    """
    return json.loads(open("config.json", "r").read())["firefox_profile_location"]

def get_headless():
    """
    Get the headless option.

    :return: The headless option.
    """
    return json.loads(open("config.json", "r").read())["headless"]

def get_verbose():
    """
    Get the verbose option.

    :return: The verbose option.
    """
    return json.loads(open("config.json", "r").read())["verbose"]
