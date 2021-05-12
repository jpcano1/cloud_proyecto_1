from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr
from ..utils import db
import uuid
import simplejson as json


class VoiceModel:
    voices = db.Table('voices')

    def create(self, value: dict):
        """
        Creates the voice in the database
        :return: The voice created
        """
        value["created"] = str(datetime.now())
        value["converted"] = False
        value["raw_audio"] = ""
        value["converted_audio"] = ""
        value["id"] = str(uuid.uuid4())
        self.voices.put_item(Item=value)
        return value

    def find(self, contest_url):
        if contest_url:
            result = self.voices.scan(
                 FilterExpression=Attr('url').eq(contest_url)
            )
        else:
            result = self.voices.scan()['Items']
        return result

    def find_one(self, id):
        return self.voices.get_item(Key={
            "id": id
        })['Item']

    def find_non_converted(self):
        return self.voices.scan(
            FilterExpression=Attr('converted').eq(False)
        )

    def update(self, id, value: dict):
        update_expression = 'SET {}'.format(','.join(f'#{k}=:{k}' for k in value))
        expression_attribute_values = {f':{k}': v for k, v in value.items()}
        expression_attribute_names = {f'#{k}': k for k in value}
        return self.voices.update_item(
            Key={
                "id":id
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names,
            ReturnValues='UPDATED_NEW',
        )

    def delete(self, id):
        return self.voices.delete_item(
            Key={
                "id":id
            }
        )

    @staticmethod
    def to_dict(voice):
        return voice