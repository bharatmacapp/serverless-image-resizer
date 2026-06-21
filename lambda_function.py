

import boto3
from PIL import Image
import os

s3 = boto3.client('s3')

DEST_BUCKET = "serverless-resized-bharath-3332"

def resize_and_upload(image, size, folder, filename):

    resized = image.copy()
    resized.thumbnail(size)

    output_path = f"/tmp/{folder}-{filename}"

    # Save image as JPEG
    resized.save(output_path, "PNG")

    # Upload with correct content type
    s3.upload_file(
        output_path,
        DEST_BUCKET,
        f"{folder}/{filename}",
        ExtraArgs={
            "ContentType": "image/PNG"
        }
    )

def lambda_handler(event, context):

    source_bucket = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']

    filename = os.path.basename(object_key)

    download_path = f"/tmp/{filename}"

    s3.download_file(
        source_bucket,
        object_key,
        download_path
    )

    image = Image.open(download_path)

    resize_and_upload(
        image,
        (200, 200),
        "small",
        filename
    )

    resize_and_upload(
        image,
        (500, 500),
        "medium",
        filename
    )

    resize_and_upload(
        image,
        (800, 800),
        "large",
        filename
    )

    return {
        "statusCode": 200,
        "body": "Images resized successfully"
    }