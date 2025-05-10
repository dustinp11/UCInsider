import os
import json
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection, helpers
from requests_aws4auth import AWS4Auth
from utils import clean_text, chunk_text

# variables 
S3_BUCKET = os.environ['RAW_S3_BUCKET']       # e.g., 'ucinsider-raw-data'
S3_PREFIX = os.environ.get('RAW_S3_PREFIX', '')  # optional prefix like 'raw/'
OS_HOST = os.environ['OPENSEARCH_HOST']     # your OpenSearch endpoint
OS_INDEX = os.environ['OPENSEARCH_INDEX']    # index name, e.g. 'uci-context'
EMBEDDING_MODEL = os.environ['EMBEDDING_MODEL_ID']  # e.g., 'amazon.titan-embed-text'
REGION = os.environ.get('AWS_REGION', 'us-west-2')


# AWS clients and opensearch setup
session = boto3.Session()

awsauth = AWS4Auth(
    ...
)

# instantiate opensearch client
os_client = OpenSearch(
    hosts=[{'host': OS_HOST, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

# download jason from s3
s3 = boto3.client('s3')
# call bedrock inference endpoints
bedrock = boto3.client('bedrock-runtime', region_name=REGION)


def get_embedding(text: str) -> list:
    """
    Call Bedrock to get text embeddings for a given chunk.
    """
    payload = {'text': text}
    resp = bedrock.invoke_model(
        modelId=EMBEDDING_MODEL,
        contentType='application/json',
        accept='application/json',
        body=json.dumps(payload)
    )
    result = json.loads(resp['body'].read())
    return result.get('embeddings', [])


def process_record(key: str):
    """
    Download JSON from S3, clean & chunk each item, embed & index.
    """
    obj = s3.get_object(Bucket=S3_BUCKET, Key=key)
    data = json.loads(obj['Body'].read())
    actions = []

    for item in data:
        post_id = item.get('id') or item.get('post_id')
        raw_text = item.get('body') or item.get('text') or ''
        cleaned = clean_text(raw_text)
        chunks = chunk_text(cleaned)

        for idx, chunk in enumerate(chunks):
            embedding = get_embedding(chunk)
            doc_id = f"{post_id}_{idx}"
            source = {
                'post_id': post_id,
                'chunk_index': idx,
                'text': chunk,
                'embedding': embedding
            }
            actions.append({
                '_index': OS_INDEX,
                '_id': doc_id,
                '_source': source
            })

    if actions:
        helpers.bulk(os_client, actions)



def lambda_handler(event, context):
    """
    AWS Lambda handler. Processes either S3 create events or batches all files under prefix.
    """
    records = event.get('Records')
    if records:
        for rec in records:
            key = rec['s3']['object']['key']
            process_record(key)
    else:
        # Batch mode: list all objects under the specified prefix
        paginator = s3.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=S3_BUCKET, Prefix=S3_PREFIX):
            for obj in page.get('Contents', []):
                process_record(obj['Key'])

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Indexing completed'})
    }




