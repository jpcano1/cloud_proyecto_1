from ..utils import db
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal
import simplejson as json
class ContestModel:
    contests = db.Table('contests')

    def create(self, value: dict):
        """
        Creates the contest in the database
        :return: The contest created
        """
        value["banner"] = ""
        value["voices"] = []
        return self.contests.put_item(Item=value)

    def find(self, email):
        if email:
            return self.contests.scan(
                FilterExpression=Attr('admin_id').eq(email)
            )['Items']
        return self.contests.scan()['Items']

    def find_one(self, url):
        response = self.contests.get_item(Key={
            "url": url
        })
        try:
            return response['Item']
        except:
            return None

    def update(self, url, value):
        update_expression = 'SET {}'.format(','.join(f'#{k}=:{k}' for k in value))
        expression_attribute_values = {f':{k}': v for k, v in value.items()}
        expression_attribute_names = {f'#{k}': k for k in value}
        return self.contests.update_item(
            Key={
                "url":url
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names,
            ReturnValues='UPDATED_NEW',
        )

    def delete(self, url):
        return self.contests.delete_item(
            Key={
                "url":url
            }
        )
    @staticmethod
    def to_dict(contest):
        return contest

