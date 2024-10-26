# middleware.py
from django.shortcuts import redirect
from django.urls import reverse

class RedirectIfNotLoggedIn:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user is authenticated
        if request.path == reverse('login') and request.user.is_authenticated:
            return redirect('home')# Redirect to login page
        response = self.get_response(request)
        return response
