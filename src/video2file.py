import os
import cv2
import json
import base64
import hashlib

from tqdm import tqdm
from pyzbar import pyzbar


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

def read_vid():
    cap = cv2.VideoCapture(src)
    cap.release()
    ret, first_frame = cap.read()
    res, retval = read_the_barc(first_frame)
    if not res:
        print("Cannot read first frame QR")
        return
    meta_data = json.loads(retval)

    dest = os.path.join(dest_folder, meta_data["Filename"])
    file = open(dest, "wb")

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

    md5_sum = checksum(dest)
    if md5_sum != meta_data["Filehash"]:
        return False
    else:
        return True

def convert_video_to_file(video_path, file_path):
    global src
    global dest_folder

    src = video_path
    dest_folder = file_path

    return read_vid()
