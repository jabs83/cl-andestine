from django.db.models import signals

from . import models


def populate_connected_users(sender, instance, action, **kwargs):
    """
    Call :populate_connected_users(): on the ``Organization`` to automatically
    add new ``Membership``'s from the incoming organization to the current one.
    """
    if isinstance(instance, models.Organization):
        if action == 'post_add' or action == 'post_clear':
            instance.populate_connected_users()


def update_or_create_organization_digest(sender, instance, created, **kwargs):
    """
    Create an ``OrganizationDigest`` each time a new ``Organization`` is created. The
    digest serves as a basic record of all organizations in the platform and
    can be used for a lookup of all recorded organizations.
    """
    if isinstance(instance, models.Organization):
        instance.update_or_create_organization_digest()
