from django.conf import settings
from django.contrib.auth.views import redirect_to_login


class RequireLoginMixin:
    def dispatch(self, request, *args, **kwargs):
        if (
            settings.ENABLE_LOGIN_REQUIRED_MIXIN
            and not request.user.is_authenticated
        ):
            return redirect_to_login(
                next=request.get_full_path(), login_url="/login"
            )
        return super(RequireLoginMixin, self).dispatch(request, *args, **kwargs)
