class MetaChoices(object):
    @classmethod
    def get_choices(cls):
        return [attr for attr in cls.__dict__ if not attr.startswith("__") and isinstance(function)]


class Hello(MetaChoices):
    Pub = 'pub'
    Cat = 'cat'

