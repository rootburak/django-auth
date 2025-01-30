from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def index(req):
    return render(req, "index.html")


def user_login(req):
    if req.user.is_authenticated:
        return redirect("index")

    if req.method == "POST":
        username = req.POST["username"]
        password = req.POST["password"]
        user = authenticate(req, username=username, password=password)
        if user is not None:
            login(req, user)
            return redirect("index")
        else:
            error = "Kullanıcı adı yada Şifre Hatalı"
            return render(req, "account/login.html", {"error": error})
    else:
        return render(req, "account/login.html")


def user_register(req):
    if req.user.is_authenticated:
        return redirect ("index")
    if req.method == "POST":
        username = req.POST["username"]
        password = req.POST["password1"]
        repassword = req.POST["password2"]
        if User.objects.filter(username=username).exists():
            return render(req, "account/register.html", {"error": "kullanıcı adı bulunmaktadır"})
        if len(str(username)) >= 5 and len(str(password)) >= 5 and password == repassword:
            user = User.objects.create_user(
                username=username, password=password)
            user.save()
            return redirect("index")
        else:
            return render(req, "account/register.html", {"error": "kullanıcı adı yada şifre 5 den büyük olmalıdır"})

    return render(req, "account/register.html")


def user_logout(req):
    logout(req)
    return redirect("index")
