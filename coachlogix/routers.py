from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)

# coachlogix.apps.organizations
from coachlogix.apps.organizations.api import OrganizationViewSet

router.register('organizations', OrganizationViewSet, base_name='organizations')
