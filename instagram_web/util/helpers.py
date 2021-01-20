import os
import boto3, botocore
import braintree
from flask import Flask, render_template, request, redirect
from app import app

# Boto3
s3 = boto3.client(
   "s3",
   aws_access_key_id=os.environ["AWS_KEY"],
   aws_secret_access_key=os.environ["AWS_SECRETKEY"]
)

def upload_profile_to_s3(file, name, acl="public-read"):

    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """

    try:

        s3.upload_fileobj(
            file,
            os.environ["BUCKET_NAME"],
            "{}/{}".format(name, file.filename),
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        print("Something Happened: ", e)
        return e

    return "{}/{}".format(name, file.filename)

def upload_images_to_s3(file, name, acl="public-read"):

    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """

    try:

        s3.upload_fileobj(
            file,
            os.environ["BUCKET_NAME"],
            "{}/images/{}".format(name, file.filename),
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        print("Something Happened: ", e)
        return e

    return "{}/images/{}".format(name, file.filename)

# Brain Tree

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=os.environ.get('BRAINTREE_MERCHANTKEY'),
        public_key=os.environ.get('BRAINTREE_PUBLICKEY'),
        private_key=os.environ.get('BRAINTREE_PRIVATEKEY') 
    )
)