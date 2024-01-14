# YouSync

A Unlimited Storage Cloud Solution, for free, built using Selenium and Python.

## Features

- Upload files
- Download files
- Delete files
- Rename files
- Search files

## Tech

- [Python](https://www.python.org/)
- [Selenium](https://www.selenium.dev/)

## Run

> ⚠️ **Have your config.json ready before trying to run the script. See [Config Section](#config) for more information.**

YouSync requires [Python](https://www.python.org/) to run.

Install the dependencies and run the script.

```bash
pip install -r requirements.txt
./run.sh --help
```

## Usage

Run the script with the `--help` or `-h` flag to see the usage.

```bash
./run.sh --help
```

## Config

Your configuration file should be named `config.json`, and should be in the same directory as the `run.sh`-
script (defaults to root directory).

Here is an example of a config file:

```json
{
  "db_provider": "mongodb",
  "sqlite_file_location": "yousync.db",
  "mongodb_db_name": "yousync",
  "mongodb_uri": "",
  "firefox_profile_location": "/home/user/.mozilla/firefox/xxxxxxx.default-release",
  "headless": false,
  "verbose": false
}
```

## How it works

To upload any file to youtube, we need to convert it to a video. To do that, YouSync uses a github repo called [`file2video`](https://github.com/karaketir16/file2video). It converts the file to a video, and then uploads it to youtube. It then gets the video id, and stores it in the specified database. You can then download the file using the provided hash, or the original file path.

## License

See [LICENSE](LICENSE) file for more information.

## Authors

- [FujiwaraChoki](https://github.com/FujiwaraChoki)