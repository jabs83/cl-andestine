from django.apps import AppConfig
from django.apps import apps
from django.db.models import signals

from . import signals as handlers


class UsersAppConfig(AppConfig):
    name = 'coachlogix.apps.users'
    verbose_name = 'Users'

    def ready(self):
        """
        Connect signals for processing changes for coachlogix.apps.users models.
        """
        # Handle new User creation and post-save processing.
        signals.post_save.connect(handlers.new_user_created,
                                  sender=apps.get_model('users', 'User'))
