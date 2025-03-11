from django.shortcuts import render
from django.views.generic import CreateView
from .models import User
from .forms import SignUpForm
from django.urls import reverse_lazy

# Create your views here.
def index(request):
    return render(request,'chatapp_app/index.html') 

class SignUpView(CreateView):
    model = User
    template_name = "chatapp_app/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy('index')
