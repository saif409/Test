from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout


def superuser_check_middleware(get_response):

    def middleware(request):
        print(request.path)
        if request.user.is_authenticated and not request.user.is_superuser:

            logout(request)
            return render(request, 'sadmin_templates/test.html')

        response = get_response(request)

        return response

    return middleware