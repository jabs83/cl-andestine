from django.apps import AppConfig
from django.apps import apps
from django.db.models import signals

from . import signals as handlers


class FilesAppConfig(AppConfig):
    name = 'coachlogix.apps.files'
    verbose_name = 'Files'

    def ready(self):
        """
        Connect signals for processing changes for coachlogix.apps.files models.
        """
        # Process a newly uploaded file and assign it a UUID along with any other
        # pre-save processing that is necessary.
        signals.pre_save.connect(handlers.process_file_upload,
                                 sender=apps.get_model('files', 'File'))
