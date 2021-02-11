allowed_extensions = {"image/jpeg", "image/png", "jpeg"}

class ContestController:
    @staticmethod
    def validate_format(format_):
        return format_ in allowed_extensions

    def __call__(self, *args, **kwargs):
        return self.validate_format(*args)