from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView

from .forms import RegisterForm


class CustomLoginView(LoginView):

    template_name = 'authentication/login.html'

    redirect_authenticated_user = True


def register_view(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect('transaction_list')

    else:

        form = RegisterForm()

    context = {
        'form': form
    }

    return render(
        request,
        'authentication/register.html',
        context
    )


def logout_view(request):

    logout(request)

    return redirect('login')