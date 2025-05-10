import os
import json
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

# Environment variables
OS_HOST = os.environ['OPENSEARCH_HOST']       # e.g., 'search-xxxxx.us-west-2.es.amazonaws.com'
OS_INDEX = os.environ['OPENSEARCH_INDEX']     # e.g., 'uci-context'
EMBEDDING_MODEL = os.environ['EMBEDDING_MODEL_ID']    # e.g., 'amazon.titan-embed-text'
COMPLETION_MODEL = os.environ['COMPLETION_MODEL_ID']  # e.g., 'anthropic.claude-instant-v1'
REGION = os.environ.get('AWS_REGION', 'us-west-2')

# Initialize AWS clients and OpenSearch connection
session = boto3.Session()
credentials = session.get_credentials()
awsauth = AWS4Auth(
    credentials.access_key,
    credentials.secret_key,
    REGION,
    'es',
    session_token=credentials.token
)

os_client = OpenSearch(
    hosts=[{'host': OS_HOST, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

bedrock = boto3.client('bedrock-runtime')


def get_embedding(text: str) -> list:
    """
    Call Bedrock to get text embeddings.
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


def search_similar(embedding: list, k: int = 5) -> list:
    """
    Perform a k-NN search in OpenSearch to retrieve top-k similar chunks.
    """
    query = {
        "size": k,
        "query": {
            "knn": {
                "embedding": {
                    "vector": embedding,
                    "k": k
                }
            }
        }
    }
    resp = os_client.search(index=OS_INDEX, body=query)
    return [hit['_source'] for hit in resp['hits']['hits']]


def generate_answer(chunks: list, question: str) -> str:
    """
    Build a prompt from context chunks and ask Claude via Bedrock.
    """
    prompt = "The following opinions are from UCI subreddit posts/comments:\n"
    for i, chunk in enumerate(chunks, start=1):
        text = chunk.get('text', '')
        prompt += f"{i}. {text}\n"
    prompt += f"\nQuestion: {question}\nAnswer:"

    payload = {
        'prompt': prompt,
        'max_tokens': 512,
        'temperature': 0.7
    }
    resp = bedrock.invoke_model(
        modelId=COMPLETION_MODEL,
        contentType='application/json',
        accept='application/json',
        body=json.dumps(payload)
    )
    result = json.loads(resp['body'].read())
    return result.get('completion', '')


def lambda_handler(event, context):
    """
    Lambda entry point for /ask endpoint.
    Expects JSON body: { "question": "..." }
    """
    try:
        body = json.loads(event.get('body', '{}'))
        question = body.get('question')
        if not question:
            return {'statusCode': 400, 'body': json.dumps({'error': 'Missing "question" in request body'})}

        # Step 1: Embed the question
        embedding = get_embedding(question)
        # Step 2: Retrieve similar context
        context_chunks = search_similar(embedding, k=5)
        # Step 3: Generate answer with Claude
        answer = generate_answer(context_chunks, question)

        return {
            'statusCode': 200,
            'headers': { 'Content-Type': 'application/json' },
            'body': json.dumps({ 'answer': answer, 'sources': context_chunks })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({ 'error': str(e) })
        }
