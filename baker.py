#!/usr/bin/env python

import argparse
import boto3
import os
import requests

def main():
    temp_file = '.temp.html'
    url = None
    aws_path = None

    parser = argparse.ArgumentParser()
    parser.add_argument('--url', '-u', dest='url')
    parser.add_argument('--aws_path', '-a', dest='aws_path')
    args = parser.parse_args()

    if not args.url:
        raise ValueError("Please provide a URL")
    else:
        url = args.url

    if not args.aws_path:
        raise ValueError("Please supply an AWS S3 bucket path")
    else:
        aws_path = args.aws_path

    r = requests.get(url, headers={'User-Agent': 'firefox'}).text


    f = open(temp_file, 'w+')
    f.write(r)
    f.close()

    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(
        temp_file,
        'cloud.registerguard.com',
        # 'ducksports/football/roster.html',
        aws_path,
        ExtraArgs = {
            'ContentType': "text/html", 'ACL': "public-read"
        }
    )

    if os.path.exists(temp_file):
        os.remove(temp_file)
    else:
        raise ValueError("File does not exist.")

if __name__ == "__main__":
    main()
