from flask import Flask, request, jsonify
import boto3
import json
from botocore.client import Config
from botocore.exceptions import ClientError
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def generate_response(user_query):
    """Takes in a user query and has Claude 3.7 sonnet generate a response based on the given context (reddit posts).
    
    Args:
        user_query (str): The give user input as a string
    Returns: 
        Nothing
    """
    
    bedrock_config = Config(connect_timeout=120, read_timeout=120, retries={'max_attempts': 0})
    bedrock_agent_client = boto3.client(
        'bedrock-agent-runtime', 
        aws_access_key_id="...", 
        aws_secret_access_key="...",
        region_name='us-west-2',
        config=bedrock_config)
    preprompt = "The format of your response should be: 1-2 sentence summary of the sentiment of the course, pros of the course (newline after pro: and then list as bullet points), cons of the course (newline after cons: and then list as bullet points), and a two sentence conclusion."
    final_query = user_query 
    
    response = bedrock_agent_client.retrieve_and_generate(
        input={
            'text': final_query
        },
        retrieveAndGenerateConfiguration={
            'type': 'KNOWLEDGE_BASE',
            'knowledgeBaseConfiguration': {
                'knowledgeBaseId': "...",
                'modelArn': "..."
            }
        }
    )
    return response['output']['text']

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_query = data.get('question', '')
    try:
        result = generate_response(user_query)
        print(result)
        return jsonify({'answer': result})
    except Exception as e:
        return jsonify({'answer': 'Backend error: ' + str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)