from ..models import AdminModel, ContestModel

allowed_extensions = {"image/jpeg", "image/png", "jpeg"}

class ContestController:
    def __init__(self):
        self.admin_model = AdminModel()
        self.contest_model = ContestModel()

    def get(self, url):
        contest = self.contest_model.find_one(url)
        if not contest:
            raise ValueError("Resource does not exist")
        return contest

    def list(self, email):
        result = self.contest_model.find(email)
        return result

    def post(self, value):
        fetched = self.contest_model.find_one(value["url"])
        if fetched:
            raise ValueError("Invalid url")
        return self.contest_model.create(value)

    def update(self, url, data):
        fetched = self.contest_model.find_one(url)
        if fetched is None:
            raise ValueError("Resource does not exist")
        self.contest_model.update(url, data)



    def delete(self, url):
        fetched = self.contest_model.find_one(url)
        if fetched is None:
            raise ValueError("Resource does not exist")
        self.contest_model.delete(url)


    @staticmethod
    def validate_format(format_):
        """
        Function to validate an image format
        :param format_: The format from parameter
        :return: The format validated if it belongs
        to the allowed file types
        :rtype: bool
        """
        return format_ in allowed_extensions