from django.shortcuts import redirect, render

from . import forms


def sign_up(request):
    form = forms.UserForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('api:sign_up')
    context = {
        'form': form
    }
    return render(request, 'users/sign_up.html', context)
