# Image Compression on AWS Lambda using Python 3.6

### Highlights
1. `Pillow==4.1.1` compiled to be usable with AWS Lambda
2. Python scripts for the actual compression

### How to use
1. Understand what is Lambda and how to use it: [Getting Started with AWS Lambda](http://docs.aws.amazon.com/lambda/latest/dg/getting-started.html). Also check out how to work with Python on AWS Lambda: [Packaging for Lambda](http://docs.aws.amazon.com/lambda/latest/dg/with-s3-example-deployment-pkg.html#with-s3-example-deployment-pkg-python)
2. Go through the architecture in the accompanying blog: [Leveraging AWS Lambda for Image Compression at scale](https://medium.com/squad-engineering/leveraging-aws-lambda-for-image-compression-at-scale-a01afd756a12)
3. Deploy [`orchestrator.py`](/orchestrator.py) and [`image_compress.py`](/image_compress.py) using AWS Lambda.
4. [Invoke the lambda](http://boto3.readthedocs.io/en/latest/reference/services/lambda.html#Lambda.Client.invoke) for `orchestrator` with a payload like:
```json
{
    "key_urls_map": {
    		"image1.jpg": "https://media.licdn.com/media/p/8/005/05b/1fb/0cf50ca.png",
    		"image2.jpg": "https://media.licdn.com/media/p/8/005/05b/1fb/0cf50ca.png"
    	},
    "quality": 90,
    "bucket_name": "compression-test-bucket"
}
```
5. Check your S3 bucket for the compressed images^
