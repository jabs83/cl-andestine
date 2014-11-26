from django.apps import AppConfig
from django.apps import apps
from django.db.models import signals

from . import signals as handlers


class OrganizationAppConfig(AppConfig):
    name = 'coachlogix.apps.organizations'
    verbose_name = 'Organizations'

    def ready(self):
        """
        Connect signals for processing changes for coachlogix.apps.organizations models.
        """
        # Due to a known bug in Django with ModelForms, we have to update the
        # connected_users cache on ``Employment`` save/delete instead of just
        # tracking the m2m_changed of the ``Organization`` model.
        # https://code.djangoproject.com/ticket/6707
        signals.m2m_changed.connect(handlers.populate_connected_users,
                                  sender=apps.get_model('organizations', 'Organization')\
                                  .connected_organizations.through)

        # Update or create an ``OrganizationDigest`` record each time an ``Organization``
        # is saved. The Digest's are used to track all records of organizations.
        signals.post_save.connect(handlers.update_or_create_organization_digest,
                                  sender=apps.get_model('organizations', 'Organization'))

