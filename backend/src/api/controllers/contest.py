allowed_extensions = {"image/jpeg", "image/png", "jpeg"}

class ContestController:
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
        return self.validate_format(*args)