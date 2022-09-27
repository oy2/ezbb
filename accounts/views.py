from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from accounts.forms import RegisterForm


# Register view
def register(request):
    # if post RegisterForm
    if request.method == 'POST':
        # form
        form = RegisterForm(request.POST)
        # if valid
        if form.is_valid():
            # save form
            user = form.save(commit=False)
            # set password
            user.set_password(form.cleaned_data['password'])
            # save form
            user.save()
            # redirect to login
            return redirect('login')
    # else
    else:
        form = RegisterForm()
    # pass form
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@login_required
def profile(request):
    # context = user
    context = {'user': request.user}
    return render(request, 'accounts/profile.html', context)