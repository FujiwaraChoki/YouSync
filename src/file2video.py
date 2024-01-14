import os
import cv2
import math
import json
import qrcode
import base64
import hashlib
import numpy as np

from tqdm import tqdm

meta_data = {}

width = 1080
height = 1080
dim = (width, height)
chunk_size = 500
frame_rate = 20.0

file_size = 0
chunk_count = 0


def read_in_chunks(file_object, chunk_size=1024):
    """
    Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k.
    
    :param file_object: The file object.
    :param chunk_size: The chunk size.

    :return: The data.
    """
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

def checksum(large_file):
    """
    Calculate the checksum of a file.

    :param large_file: The file path.

    :return: The checksum.
    """
    md5_object = hashlib.md5()
    block_size = 128 * md5_object.block_size
    a_file = open(large_file, 'rb')
    chunk = a_file.read(block_size)
    while chunk:
        md5_object.update(chunk)
        chunk = a_file.read(block_size)
    md5_hash = md5_object.hexdigest()

    return md5_hash

def create_qr(data_str):
    """
    Create a QR code.

    :param data_str: The data to encode.

    :return: The QR code.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=4,
    )
    qr.add_data(data_str)
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    cv_img = np.array(img)
    return cv_img[:, :, ::-1].copy()

def create_video():
    """
    Create a video from a file.

    :return: None
    """
    global meta_data
    global file_size
    global chunk_count

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(dest, fourcc, frame_rate, dim)

    md5_checksum = checksum(src)
    file_stats = os.stat(src)
    file_size = file_stats.st_size
    chunk_count = math.ceil(file_size / chunk_size)


    meta_data["Filename"] = os.path.basename(src)
    meta_data["ChunkCount"] = chunk_count
    meta_data["Filehash"] = md5_checksum

    first_frame = create_qr(json.dumps(meta_data, indent=4))
    first_frame = cv2.resize(first_frame, dim, interpolation=cv2.INTER_AREA)
    out.write(first_frame)

    pbar = tqdm(total=chunk_count)
    with open(src, 'rb') as f:
        for piece in read_in_chunks(f, chunk_size):
            frame = create_qr(base64.b64encode(piece).decode('ascii'))
            frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
            out.write(frame)
            pbar.update(1)
    pbar.close()


    # Release everything if job is finished
    out.release()

def convert_file_to_video(file_path, output_file_path):
    """
    Convert a file to a video.

    :param file_path: The file path.
    :param output_file_path: The output file path.

    :return: None
    """

    # Define global variables
    global src
    global dest

    # Set global variables
    src = file_path
    dest = output_file_path

    # Create the video
    create_video()
