from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.settings import api_settings

from coachlogix.base.api.viewsets import CrudModelViewSet

from . import models
from . import providers
from . import serializers


class FileViewSet(CrudModelViewSet):
    queryset = models.File.objects.all()
    serializer_class = serializers.FileSerializer
    parser_classes = (FormParser, MultiPartParser,)

    def pre_save(self, obj):
        """Set the object's owner, based on the incoming request."""
        obj.owner = self.request.user

    def retrieve(self, request, *args, **kwargs):
        """
        This method is called on a :GET: request.

        It first checks to see if the ``File`` has a provider document id
        and a query string called :preview: was attached to the request.

        If both conditions are met it moves to the second conditional which
        checks if an existing valid and non-expired Box view exists. If it
        doesn't then it calls the Box API and fetches a new one.
        """
        self.obj = self.get_object()
        
        # Get the provider document id from the file.
        try:
            doc_id = self.obj.provider.doc_id
        except AttributeError:
            doc_id = None

        if request.QUERY_PARAMS.get('preview', None) is not None and doc_id:

            # See if an existing valid view exists, call Box.com API if not.
            url = self.obj.provider.view_url
            
            if not url or self.obj.provider.is_view_expired:
                url = providers.box.create_session(self.obj, doc_id)

            self.resource_name = False
            return Response(data={'url': url}, status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(self.obj)
            return Response(serializer.data)
        
