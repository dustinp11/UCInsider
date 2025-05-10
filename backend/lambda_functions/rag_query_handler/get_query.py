import boto3
import json

# 1) Use us-west-2
bedrock = boto3.client(
    'bedrock-runtime',
    region_name='us-west-2'

)

# 2) Build your request body
body = json.dumps({
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 1000,
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Hello What is happiness?"
                }
            ]
        }
    ]
})

# 3) Point modelId at your us-west-2 inference profile ARN
modelId = ...

accept      = 'application/json'
contentType = 'application/json'

# 4) Invoke and print
response = bedrock.invoke_model(
    modelId=modelId,
    contentType=contentType,
    accept=accept,
    body=body
)

result = json.loads(response['body'].read())
assistant_text = result['content'][0]['text']
print(assistant_text)