from django.shortcuts import redirect

def active_profile_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.profile.is_active:
            return redirect('profile')
        return view_func(request, *args, **kwargs)
    return wrapper