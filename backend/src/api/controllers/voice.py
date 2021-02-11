allowed_extensions = {
    "audio/ogg", "audio/wav",
    "audio/oga", "audio/m4a",
    "audio/aac", "audio/wma",
    "audio/wave", "audio/mp3"
}

class VoiceController:
    @staticmethod
    def validate_format(format_):
        return format_ in allowed_extensions

    def __call__(self, *args, **kwargs):
        return self.validate_format(*args)