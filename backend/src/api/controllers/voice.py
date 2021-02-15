allowed_extensions = {
    "audio/ogg", "audio/wav",
    "audio/oga", "audio/m4a",
    "audio/aac", "audio/wma",
    "audio/wave", "audio/mp3"
}

class VoiceController:
    @staticmethod
    def validate_format(format_):
        """
        Function to validate a sound format
        :param format_: The format from parameter
        :return: The format validated if it belongs
        to the allowed file types
        :rtype: bool
        """
        return format_ in allowed_extensions

    def __call__(self, *args, **kwargs):
        return self.validate_format(*args)