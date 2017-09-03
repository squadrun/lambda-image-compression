# lambda-image-compression

This repository contains:
1. Zipped site-packages containing Pillow compatible with AWS Lambda and Python 3.6
2. Code for Lambda function to compress images: `image_compression.py`
3. Code for an Orchestrator Lambda function that takes a list of URLs and calls the function in `image_compression.py` for each URL.
