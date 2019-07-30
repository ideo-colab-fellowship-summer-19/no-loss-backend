'''

Core logic executed in each of the routes.

'''



import boto3
from boto3.dynamodb.conditions import Key, Attr
import boto3.session
from botocore.exceptions import ClientError
import os
from os import environ
from decimal import *
from random import randint
import random
import uuid
#from config import S3_KEY, S3_SECRET, S3_BUCKET
from application import ENV, PROD_ENV, DEV_ENV

# s3 = boto3.client(
#    "s3",
#    aws_access_key_id=S3_KEY,
#    aws_secret_access_key=S3_SECRET
# )
USERS_TABLE_PRODUCTION = 'MonthlyUsers'
USERS_TABLE_DEV = 'MonthlyUsers-dev'

PROJECTS_TABLE_PRODUCTION = 'Projects'
PROJECTS_TABLE_DEV = 'Projects-dev'

CLASSESSTATE_TABLE_PRODUCTION = 'ClassesState'
CLASSESSTATE_STATE_DEV = 'ClassesState-dev'

PEERGROUPS_TABLE_PRODUCTION = 'PeerGroups'
PEERGROUPS_TABLE_DEV = 'PeerGroups-dev'


USERS_TABLE = USERS_TABLE_PRODUCTION if ENV == PROD_ENV else USERS_TABLE_DEV
CLASSESSTATE_TABLE = CLASSESSTATE_TABLE_PRODUCTION if ENV == PROD_ENV else CLASSESSTATE_STATE_DEV
PEERGROUPS_TABLE = PEERGROUPS_TABLE_PRODUCTION if ENV == PROD_ENV else PEERGROUPS_TABLE_DEV

PROJECTS_TABLE = PROJECTS_TABLE_PRODUCTION if ENV == PROD_ENV else PROJECTS_TABLE_DEV

# GENERAL SECTION


def dbSetup():
    # Get the service resource.
    DYNAMODB_ACCESS_KEY = environ.get('DYNAMODB_ACCESS_KEY')
    DYNAMODB_SECRET_KEY = environ.get('DYNAMODB_SECRET_KEY')
    SENDGRID_API_KEY = environ.get('SENDGRID_API_KEY')
    os.environ['AWS_DEFAULT_REGION'] = "us-east-2"
    #global dynamodb
    # if dynamodb == None:
    session = boto3.session.Session()
    dynamodb = session.resource('dynamodb', aws_access_key_id=DYNAMODB_ACCESS_KEY,
                                aws_secret_access_key=DYNAMODB_SECRET_KEY)
    return dynamodb
