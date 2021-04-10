from ..models import AdminModel, ContestModel

allowed_extensions = {"image/jpeg", "image/png", "jpeg"}

class ContestController:
    def __init__(self, admin_id):
        self.admin_id = admin_id
        self.admin_model = AdminModel()
        self.contest_model = ContestModel()

    def get(self, url):
        return self.contest_model.find_one(url)

    def list(self, admin_id):
        return self.contest_model.find(admin_id)

    def post(self, value):
        return self.contest_model.create(value)

    def update(self, url, admin_id, data):
        return self.contest_model.update(url, admin_id, data)

    def delete(self, url, admin_id):
        return self.contest_model.delete(url, admin_id)

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

    def __call__(self, *args, **kwargs):
        """
        This function is called when the ContestController
        object is called
        :param args: The function arguments
        :param kwargs: The function keyword arguments
        :return: The result of the validation
        """
        return self.validate_format(*args)