from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from functools import wraps
from .models import UserProfile

def seller_required(view_func):
    @login_required
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            if request.user.userprofile.user_type != 'seller':
                return redirect('index')
        except UserProfile.DoesNotExist:
            return redirect('index')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
