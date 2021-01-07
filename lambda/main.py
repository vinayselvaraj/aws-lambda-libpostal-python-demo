import os
import glob
import boto3
import json
import tempfile

from io import BytesIO
from pyzbar.pyzbar import decode
from PIL import Image

s3 = boto3.client('s3')

def handler(event, context):
    s3_bucket = event['s3_bucket']
    s3_object = event['s3_object']

    entries = list()

    imgfile = tempfile.TemporaryFile()
    s3.download_fileobj(s3_bucket, s3_object, imgfile)
    pil_image = Image.open(imgfile)
    num_frames = getattr(pil_image, "n_frames", 1)

    for i in range(num_frames):
        pil_image.seek(i)

        barcodes = decode(pil_image)

        for barcode in barcodes:
            barcode_entry = dict()
            barcode_entry['data'] = barcode.data.decode('utf-8')
            barcode_entry['type'] = barcode.type
            entries.append(barcode_entry)

    # img_bytes = s3.get_object(Bucket=s3_bucket, Key=s3_object)['Body'].read()
    # barcodes = decode(Image.open(BytesIO(img_bytes)))
    
    
    
    imgfile.close()

    return json.dumps(entries)