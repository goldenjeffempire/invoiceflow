from functools import wraps
from django.core.exceptions import PermissionDenied

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not getattr(request.user, 'is_admin', lambda: False)():
            raise PermissionDenied()
        return view_func(request, *args, **kwargs)
    return _wrapped_view
