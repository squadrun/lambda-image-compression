import requests
import boto3

from PIL import Image
from io import BytesIO
from requests import RequestException

s3_client = boto3.client('s3')
output_path = '/tmp/output_file'


class UnaccessibleUrlException(Exception):
    pass


def get_compressed_image_url(source_image_url, filename, bucket_name, quality=95, image_width=500):
    try:
        response = requests.get(source_image_url)
        if not response.ok:
            raise UnaccessibleUrlException
    except (UnaccessibleUrlException, RequestException):
        print("Broken URL:{0}".format(source_image_url))
        with open(output_path, 'w') as f:
            f.write('')
        s3_client.upload_file(output_path, bucket_name, filename + ".broken")
    else:
        try:
            image_obj = Image.open(BytesIO(response.content))
            compress_image_obj(image_obj, quality, image_width, filename, bucket_name)
        except Exception as exc:
            print("Exception:{0} - {1}".format(exc.__class__.__name__, exc))

    return True


def compress_image_obj(image_obj, quality, image_width, filename, bucket_name):
    width, height = image_obj.size
    new_size = (int(image_width), int(float(height) * float(image_width) / float(width)))

    # don't resize in case image's width is smaller than specified width since that would lead to stretched image
    if width > image_width:
        mode = image_obj.mode
        if mode == 'RGBA' or mode == 'RGBa':
            # A/a is the Alpha channel. If it is present then to
            # to preserve transparency, paste the image over a white background
            image_obj = image_obj.resize(new_size, Image.ANTIALIAS)
            background_layer = Image.new('RGB', new_size, (255, 255, 255))
            background_layer.paste(image_obj, image_obj)
            image_obj = background_layer.convert('RGB')
        else:
            image_obj = image_obj.resize(new_size, Image.ANTIALIAS)
    image_obj.save(output_path, 'JPEG', quality=quality)

    s3_client.upload_file(output_path, bucket_name, filename)

    return True


def lambda_handler(event, context):
    source_image_url, filename = event['source_image_url'], event['filename']
    quality, bucket_name = event['quality'], event['bucket_name']
    get_compressed_image_url(source_image_url, filename, bucket_name, quality)
    return True
