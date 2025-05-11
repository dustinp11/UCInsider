# from flask import Flask, request, jsonify
import boto3
import json
from botocore.client import Config
from botocore.exceptions import ClientError
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)


def generate_response(user_query, modelArn, access_key, secret_access_key, region_name):
    """Takes in a user query and has Claude 3.7 sonnet generate a response based on the given context (reddit posts).
    
    Args:
        user_query (str): The give user input as a string
    Returns: 
        Nothing
    """
    
    bedrock_config = Config(connect_timeout=120, read_timeout=120, retries={'max_attempts': 0})
    bedrock_agent_client = boto3.client(
        'bedrock-agent-runtime', 
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_access_key,
        region_name=region_name,
        config=bedrock_config)
    preprompt = "Give detailed response"
    final_query = user_query 
    
    response = bedrock_agent_client.retrieve_and_generate(
        input={
            'text': final_query
        },
        retrieveAndGenerateConfiguration={
            'type': 'KNOWLEDGE_BASE',
            'knowledgeBaseConfiguration': {
                'knowledgeBaseId': "...",
                'modelArn': modelArn
            }
        }
    )
    return response['output']['text']

def summarize_with_haiku(result, modelID, access_key, secret_access_key, region_name):
    pre_prompt = (f"Summarize this response in 2-3 sentences. Make sure explicitly refer to any professor's name listed: {result}")

    bedrock_runtime = boto3.client(
        "bedrock-runtime",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_access_key,
        region_name=region_name
    )

    kwargs = {
        "modelId": modelID,
        "contentType": "application/json",
        "accept": "application/json",
        "body": json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 500,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": pre_prompt
                        }
                    ]
                }
            ]
        })
    }

    response = bedrock_runtime.invoke_model(**kwargs)
    result = json.loads(response["body"].read())
    return result["content"][0]["text"]

# @app.route('/ask', methods=['POST'])
# def ask():
#     data = request.get_json()
#     user_query = data.get('question', '')
#     try:
#         result = generate_response(user_query, "...", "...",
#                                    '...')
#         summary = summarize_with_haiku(result, "...", '...')
#         return jsonify({'answer': summary})
#     except Exception as e:
#         return jsonify({'answer': 'Backend error: ' + str(e)}), 500

if __name__ == '__main__':
    # app.run(port=5000, debug=True)
    user_query = "is ICS 33 difficult?"
    #     user_query = data.get('question', '')
    result = generate_response(user_query, "...",
                               "...", "...",
                               '...')
    print("result:", result)
    summary = summarize_with_haiku(result, "...", "...",
                                   "...", '...')
    print("summary:", summary)