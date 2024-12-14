from django.shortcuts import render , redirect
from .forms import UserRegisterForm ,ConnexionForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.forms import PasswordChangeForm 
from .models import Profil
from django.contrib.auth.models import User
# Create your views here.
from django.contrib.auth import authenticate, login

# Create your views here.

def base(request):
    return render(request,'user/base.html')

def login(request,id):
    error = False

    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password) 
            if user :  
                if username != 'admin':
                    profil = Profil.objects.filter(user=user)
                    return redirect('http://127.0.0.1:8000/evaluer/')
                else:
                    if id != '0':
                        return redirect('http://127.0.0.1:8000/'+id+'/')
            else: 
                error = True
    else:
        form = ConnexionForm()

    return render(request, 'user/login.html', {'form': form,'id':id,'error':error})

def logout(request):
    return render(request,'user/logout.html')

def signup(request,id):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            type_utilisateur = request.POST.get('type_utilisateur')
            user = User.objects.get(username=username)
            profil = Profil(user=user,type_utilisateur=type_utilisateur)
            profil.save()
            messages.success(request, 'ton compte est crrer vous pouver mainteneant vous connecter')
            return redirect('http://127.0.0.1:8000/login/'+id+'/')
    else:
        form = UserRegisterForm()
    return render(request, 'user/signup.html',{'form': form,'id':id})





