import boto3
import json


lambda_client = boto3.client('lambda')


def send_url_for_compression(url, filename, quality, bucket_name):
    payload = {
        "source_image_url": url,
        "filename": filename,
        "quality": quality,
        "bucket_name": bucket_name
    }
    lambda_client.invoke(
        FunctionName="image_compress",
        InvocationType='Event',
        Payload=json.dumps(payload)
    )


def lambda_handler(event, context):
    key_urls_map = event['key_urls_map']
    quality, bucket_name = event['quality'], event['bucket_name']

    for key, url in key_urls_map.items():
        send_url_for_compression(url, key, quality, bucket_name)

    return True
