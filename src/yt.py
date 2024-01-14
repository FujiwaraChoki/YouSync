import os
import cv2
import json
import time
import base64
import hashlib

from config import *
from tqdm import tqdm
from pyzbar import pyzbar
from pytube import YouTube
from termcolor import colored
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

FIREFOX_PROFILE_LOCATION = get_firefox_profile_location()
HEADLESS = get_headless()
VERBOSE = get_verbose()

def build_url(video_id):
    """
    Build a YouTube video URL from a video ID.

    :param video_id: The video ID.

    :return: The YouTube video URL.
    """
    return f"https://www.youtube.com/watch?v={video_id}"

def prep_video(src):
    """
    Prepares a video for uploading to YouTube (resolution, frame rate, etc.) using moviepy.

    :param src: The source file path.

    :return: The prepared video path.
    """
    if VERBOSE:
        print(colored(f"\n[+] Preparing video for YouTube...", "light_cyan"))

    video = VideoFileClip(src)

    original_duration = video.duration

    # Combine video with black image
    black_image = (ImageClip("assets/black_image.png"))
    video = CompositeVideoClip([black_image, video.set_position("center")]).set_duration(video.duration + 30)

    # Write video to temporary file
    if not VERBOSE:
        video.write_videofile(src, codec="libx264", audio_codec="aac", logger=None)
    else:
        video.write_videofile(src, codec="libx264", audio_codec="aac")

    if VERBOSE:
        print(colored(f"[+] Prepared video for YouTube: {src}", "light_green"))

    # Get full path of src
    src = os.path.abspath(src)

    return original_duration, src

def upload_video(src, hash_id, original_file_name):
    """
    Upload a video to YouTube.

    :param src: The source file path.
    :param hash_id: The UUID string.
    :param original_file_name: The original file name.

    :return: The YouTube video URL.
    """
    try:
        duration, updated_path = prep_video(src)

        print(colored(f"\n[+] Uploading video to YouTube...", "light_cyan"))

        # Set options
        options = Options()
        
        if HEADLESS:
            options.add_argument("--headless")

        # Instantiate Webdriver using Firefox profile
        fp = webdriver.FirefoxProfile(FIREFOX_PROFILE_LOCATION)
        driver = webdriver.Firefox(firefox_profile=fp, firefox_options=options)

        # Navigate to YouTube
        driver.get("https://www.youtube.com/upload")

        # Set video file
        FILE_PICKER_TAG = "ytcp-uploads-file-picker"
        file_picker = driver.find_element(By.TAG_NAME, FILE_PICKER_TAG)
        INPUT_TAG = "input"
        file_input = file_picker.find_element(By.TAG_NAME, INPUT_TAG)
        file_input.send_keys(updated_path)

        # Wait for upload to finish
        time.sleep(5)

        # Set title & description
        TEXTBOX_ID = "textbox"
        textboxes = driver.find_elements(By.ID, TEXTBOX_ID)

        title_el = textboxes[0]
        description_el = textboxes[-1]

        if VERBOSE:
            print(colored("\t=> Setting title...", "yellow"))
        title_el.click()
        time.sleep(0.5)
        title_el.clear()
        title_el.send_keys(str(duration) + "::::" + original_file_name)

        if VERBOSE:
            print(colored("\t=> Setting description...", "yellow"))
        time.sleep(0.5)
        description_el.click()
        time.sleep(0.5)
        description_el.clear()
        description_el.send_keys(hash_id)
        
        time.sleep(0.5)

        # Set `made for kids` option
        if VERBOSE:
            print(colored("\t=> Setting `made for kids` option...", "yellow"))
        MADE_FOR_KIDS_NAME = "VIDEO_MADE_FOR_KIDS_MFK"
        NOT_MADE_FOR_KIDS_NAME = "VIDEO_MADE_FOR_KIDS_NOT_MFK"

        is_for_kids_checkbox = driver.find_element(By.NAME, MADE_FOR_KIDS_NAME)
        is_not_for_kids_checkbox = driver.find_element(By.NAME, NOT_MADE_FOR_KIDS_NAME)

        if True:
            is_not_for_kids_checkbox.click()
        else:
            is_for_kids_checkbox.click()

        time.sleep(0.5)

        # Click next
        if VERBOSE:
            print(colored("\t=> Clicking next...", "yellow"))
        NEXT_BUTTON_ID = "next-button"
        next_button = driver.find_element(By.ID, NEXT_BUTTON_ID)
        next_button.click()

        # Click next again
        print(colored("\t=> Clicking next again...", "yellow"))
        next_button = driver.find_element(By.ID, NEXT_BUTTON_ID)
        next_button.click()
        
        # Wait for 2 seconds
        time.sleep(2)

        # Click next again
        if VERBOSE:
            print(colored("\t=> Clicking next again...", "yellow"))
        next_button = driver.find_element(By.ID, NEXT_BUTTON_ID)
        next_button.click()


        # Set as unlisted
        if VERBOSE:
            print(colored("\t=> Setting as unlisted...", "yellow"))
        RADIO_BUTTON_XPATH = '//*[@id="radioLabel"]'
        radio_button = driver.find_elements(By.XPATH, RADIO_BUTTON_XPATH)
        radio_button[1].click()


        if VERBOSE:
            print(colored("\t=> Clicking done button...", "yellow"))
        # Click done button
        DONE_BUTTON_ID = "done-button"
        done_button = driver.find_element(By.ID, DONE_BUTTON_ID)
        done_button.click()

        # Wait for 2 seconds
        time.sleep(2)

        # Get latest video
        if VERBOSE:
            print(colored("\t=> Getting video URL...", "yellow"))

        driver.get("https://studio.youtube.com/channel/UC1ghEiTed2YQhLY1YNouzfQ/videos/")
        time.sleep(2)
        videos = driver.find_elements(By.TAG_NAME, "ytcp-video-row")
        first_video = videos[0]
        anchor_tag = first_video.find_element(By.TAG_NAME, "a")
        href = anchor_tag.get_attribute("href")
        if VERBOSE:
            print(colored(f"\t=> Extracting video ID from URL: {href}", "yellow"))
        video_id = href.split("/")[-2]

        # Build URL
        url = build_url(video_id)

        # Close driver
        driver.close()

        if VERBOSE:
            print(colored(f"[+] Uploaded to YouTube: {url}", "light_green"))

        return url
    except Exception as error:
        print(colored(f"\n[-] An error occurred while uploading the video to YouTube: {error}", "light_red"))

def checksum(large_file):
    md5_object = hashlib.md5()
    block_size = 128 * md5_object.block_size
    a_file = open(large_file, 'rb')
    chunk = a_file.read(block_size)
    while chunk:
        md5_object.update(chunk)
        chunk = a_file.read(block_size)
    md5_hash = md5_object.hexdigest()

    return md5_hash


def read_the_barc(frame):
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        barcode_info = barcode.data.decode('utf-8')
        return True, barcode_info
    return False, 0

def download_video(url, output_path):
    """
    Download a YouTube video by URL.

    :param url: The YouTube video URL.
    :param output_path: The output path.

    :return: None
    """
    if VERBOSE:
            print(colored(f"\n[+] Downloading video from YouTube...", "light_cyan"))
    print(colored(url, "light_green"))
    video = YouTube(url)
    best = video.streams.get_highest_resolution()

    # Cut duration
    duration = float(video.title.split("::::")[0])

    try:
        best.download(filename=output_path)
    except Exception as e:
        print(colored(f"[-] Failed to download video from YouTube: {e}", "light_red"))
        return

    # Set Duration
    clip = VideoFileClip(output_path)
    clip = clip.subclip(0, float(duration))
    if not VERBOSE:
        clip.write_videofile(output_path, codec="libx264", audio_codec="aac", logger=None)
    else:
        clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

    time.sleep(2)
    
    cap = cv2.VideoCapture(output_path)
    ret, first_frame = cap.read()
    res, retval = read_the_barc(first_frame)
    if not res:
        print(colored("[-] Can't parse first frame of QR Code.", "light_red"))
        return
    meta_data = json.loads(retval)

    file = open(output_path, "wb")

    pbar = tqdm(total=meta_data["ChunkCount"])
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            res, retval = read_the_barc(frame)
            assert res
            file.write(base64.b64decode(retval))
            pbar.update(1)
        else:
            break

    pbar.close()
    file.close()
    
    # md5_sum = checksum(output_path)
    if VERBOSE:
        print(colored(f"[+] Downloaded video from YouTube: {video.title}", "light_green"))
