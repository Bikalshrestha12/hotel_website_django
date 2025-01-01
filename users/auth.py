from django.shortcuts import redirect

# to check the user is login or not

def unauthentcated_user(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        # elif request.user.is_owner:
        #     return redirect("/owner")
        else:
            return view_function(request, *args, **kwargs)
    return wrapper_function

# to check wheather the user is admin or not.

def admin_only(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_staff:
            return view_function(request, *args, **kwargs)
        else:
            return redirect('/admins')
    return wrapper_function