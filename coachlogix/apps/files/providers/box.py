import os
import json
import boxview

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from common.files.models import ProviderRecord
from common.files.exceptions import FileUploadError

api = boxview.BoxView(settings.BOX_VIEW_API_KEY)
BoxViewError = boxview.BoxViewError


def process_upload(fobj):
    """Connect to the Box.com API and create a new ``FileRecord``."""
    try:
        doc = api.create_document(file=fobj.path, name=fobj.name)
    except BoxViewError, e:
        error = json.loads(e._get_error())
        message = error['details'][0]['message']
        raise FileUploadError(_(message))
    else:
        # Create a new provider and add them to the file record.
        provider = ProviderRecord()
        provider.name = provider.BOX
        provider.status = doc.get('status', None)
        provider.doc_id = doc.get('id', None)
        provider.doc_type = doc.get('type', None)
        provider.save()

        fobj.provider = provider
        fobj.save()


def create_session(fobj, doc_id):
    """Connect to the Box.com API and create a session."""
    if not api.ready_to_view(doc_id):
        return

    session = api.create_session(doc_id, duration=settings.BOX_SESSION_DURATION)
    
    if session.get('id', None) is not None:
        try:
            fobj.provider.view_url = session.get('urls', {}).get('view', None)
            fobj.provider.view_expiration = session.get('expires_at', None)
        except AttributeError, ValueError:
            return
        else:
            fobj.provider.save()
            return fobj.provider.view_url
        
