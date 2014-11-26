from django.utils.translation import ugettext_lazy as _


STARTED = 0
ACTIVE = 1
PAUSED = 2
COMPLETE = 3
STATUS_CHOICES = (
    (STARTED, _('started')),
    (ACTIVE, _('active')),
    (PAUSED, _('paused')),
    (COMPLETE, _('complete')),
)
