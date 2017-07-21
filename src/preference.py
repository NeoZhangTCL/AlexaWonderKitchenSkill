import boto3
import json

dynamodb = boto3.resource('dynamodb', region_name='eu-west-1', endpoint_url="http://localhost:8000")

table = dynamodb.Table('Preference')

def set_recipe_preference(user_id, recipe_id, feedback):

    try:
        get_response = table.query(
            KeyConditionExpression=Key('user_id').eq(user_id)
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        reviews = get_response['Items']

        score = 0
        for r in reviews:
            if r['recipe_id'] == recipe_id:
                score = r['score']
                break

        score += feedback
        put_response = table.put_item(
            Item={
                'user_id': user_id,
                'recipe_id': recipe_id,
                'score': score
            }
        )

        print("PutItem succeeded:")
        print(json.dumps(response, indent=4))
