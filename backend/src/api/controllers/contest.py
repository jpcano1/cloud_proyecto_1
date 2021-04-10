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

    def list(self, admin_id):
        return self.contest_model.find(admin_id)

    def post(self, value):
        return self.contest_model.create(value)

    def update(self, url, admin_id, data):
        result = self.contest_model.update(url, admin_id, data)
        if result.matched_count < 1:
            raise ValueError("Resource does not exist")

    def delete(self, url, admin_id):
        result = self.contest_model.delete(url, admin_id)
        if result.deleted_count < 1:
            raise ValueError("Resource does not exist")

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