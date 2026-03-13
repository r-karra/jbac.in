from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from accounts.models import User


class EmailOrMobileBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, role=None, **kwargs):
        identifier = username or kwargs.get("identifier")
        if not identifier or not password:
            return None

        user = (
            User.objects.filter(Q(mobile_number=identifier) | Q(email__iexact=identifier))
            .distinct()
            .first()
        )
        if user is None:
            return None
        if role and user.role != role:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None