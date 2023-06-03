# Create your views here.

# Create your views here.

from django.shortcuts import redirect
from django.shortcuts import render
# Create your views here.
from django.views.generic import TemplateView

from .forms import SignupForm


class HomePageView(TemplateView):
    template_name = 'home.html'


# def signup(request):
#    if request.method == 'POST':
#        form = SignupForm(request.POST)
#        if form.is_valid():
#            form.save()
#            return redirect('')  # Replace 'home' with the URL name of your desired success page
#    else:
#        form = SignupForm()
#
#    return render(request, 'signup.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin:index')  # Replace 'home' with the URL name of your desired success page
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})
