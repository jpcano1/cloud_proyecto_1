from ..utils import db

# Encryption Libraries
from flask_bcrypt import generate_password_hash, check_password_hash


class AdminModel:
    admins = db.Table('admins')

    def create(self, value: dict):
        """
        Creates the admin in the database
        :return: The admin created
        """
        value["contests"] = []
        self.admins.put_item(Item=value)
        return value

    def find_one(self, email):
        response = self.admins.get_item(Key={
            "email": email
        })

        try:
            return response['Item']
        except:
            return None

    def find(self):
        return self.admins.scan()['Items']

    def update(self, email, value: dict):
        update_expression = 'SET {}'.format(','.join(f'#{k}=:{k}' for k in value))
        expression_attribute_values = {f':{k}': v for k, v in value.items()}
        expression_attribute_names = {f'#{k}': k for k in value}
        return self.admins.update_item(
            Key={
                "email": email
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names,
            ReturnValues='UPDATED_NEW',
        )

    def find_by_email(self, email):
        """
        Finds admin user by email in the database
        :param email: The email of the user to be found
        :param password: The password of the user to be
        authenticated
        :return: The user found, else None
        """
        response = self.admins.get_item(Key={
            "email": email
        })

        try:
            return response['Item']
        except:
            return None

    @staticmethod
    def generate_hash(password):
        """
        Generates the hash for the password in order
        to encrypt the password in the database
        :param password: The password to be hashed
        :return: The hash of the encrypted password
        """
        return generate_password_hash(password).decode("utf-8")

    @staticmethod
    def verify_hash(hash_, password):
        """
        Verifies the hash from the password in the
        database with the password coming from login
        :param hash_: The hashed password in the database
        :param password: The password to be verified
        :return: The verification, True if correct,
        False if incorrect
        :rtype: bool
        """
        return check_password_hash(hash_, password)

    @staticmethod
    def to_dict(admin: dict):
        admin.pop("password")
        return admin
