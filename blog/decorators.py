# decorators.py

from functools import wraps
from django.shortcuts import redirect
from .models import Subscription


def subscription_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user_subscription = Subscription.objects.get(user=request.user)
        if user_subscription.active:
            return view_func(request, *args, **kwargs)
        else:
            # Redirect to a page indicating that blog posting is restricted
            return redirect('restricted_access')
    return _wrapped_view
