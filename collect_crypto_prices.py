from datetime import datetime, timezone
import requests
import logging
import csv
import json
import boto3


S3_BUCKET = 'crypto-tracking'
S3_CLIENT = boto3.client('s3')
TIMESTAMP = datetime.now(tz=timezone.utc).strftime('%H:%M:%S')
LOCAL_PATH = f'/tmp/{TIMESTAMP}.csv'


def get_key():
    date = datetime.now(tz=timezone.utc)
    key = f'raw/{date.year}/{date.month}/{date.day}/{TIMESTAMP}.csv'

    return key


def upload_file():
    key = get_key()
    
    with open(LOCAL_PATH, 'rb') as file:
        S3_CLIENT.put_object(Bucket=S3_BUCKET, Key=key, Body=file)
    
    return print('File uploaded')


def extract_data():
    #API request, no key is needed
    url = "https://api.coincap.io/v2/assets"
    
    try:
        r = requests.get(url)
    except requests.ConnectionError as ce:
        logging.error(f"There was an error with the request, {ce}")
        sys.exit(1)
        
    data = r.json()
    return data
    
def transform_data(data):
    header = []
    prices = []
    for i, coin in enumerate(data['data']):
        if i == 0:
            header.append('TIME')
            prices.append(f'{TIMESTAMP}')
            continue

        header.append(coin['symbol'])
        prices.append(coin['priceUsd'])
        
    with open(LOCAL_PATH, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerow(prices)

    return print('Data gathered')

    

def lambda_handler(event, context):
    #Extract
    data = extract_data()
    
    #Transform
    transform_data(data)
    
    #Load
    upload_file()
