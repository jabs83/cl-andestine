from rest_framework import serializers

from coachlogix.apps.users.models import User

from . import models


class MembershipSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Membership
        fields = (
            'pk',
            'organization',
            'groups',
            'user',
            'role',
            'title',
            'connected_by',
            'is_employee',
        )


class MemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'pk',
            'first_name',
            'last_name',
            'email',
        )


class OrganizationSerializer(serializers.ModelSerializer):
    memberships = MembershipSerializer(read_only=True, many=True)
    members = MemberSerializer(read_only=True, many=True)

    class Meta:
        model = models.Organization
