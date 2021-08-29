from rest_framework import viewsets


class ReadWriteModelViewSet(viewsets.ModelViewSet):
    write_serializer_class = None
    read_actions = ['list', 'retrieve']
    write_actions = ['create', 'partial_update', 'destroy']

    def get_serializer_class(self):
        if self.action in self.read_actions:
            assert self.serializer_class is not None, (
                    "'%s' should either include a `serializer_class` attribute, "
                    "or override the `get_serializer_class()` method."
                    % self.__class__.__name__
            )
            return self.serializer_class
        else:
            assert self.write_serializer_class is not None, (
                    "'%s' should either include a `write_serializer_class` attribute, "
                    "or override the `get_serializer_class()` method."
                    % self.__class__.__name__
            )
            return self.write_serializer_class
