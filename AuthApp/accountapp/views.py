from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages


def index(req):
    return render(req, "index.html")


@login_required()
def products(req):
    return render(req, "account/products.html")


@user_passes_test(lambda e: e.is_superuser)
def admin_products(req):
    return render(req, "account/admin_products.html")


def user_login(req):
    if req.user.is_authenticated:
        return redirect("index")

    if req.method == "POST":
        username = req.POST["username"]
        password = req.POST["password"]
        user = authenticate(req, username=username, password=password)
        if user is not None:
            messages.success(req, "Giriş Başarılı")
            login(req, user)
            return redirect("index")
        else:
            messages.error(req, "Kullanıcı adı ya da şifre hatalı")
            return render(req, "account/login.html")
    else:
        return render(req, "account/login.html")


def user_register(req):
    if req.user.is_authenticated:
        return redirect("index")

    if req.method == "POST":
        username = req.POST["username"]
        password = req.POST["password1"]
        repassword = req.POST["password2"]

        if User.objects.filter(username=username).exists():
            messages.error(req, "Kullanıcı adı bulunmaktadır")
            return render(req, "account/register.html")

        if len(username) < 5 or len(password) < 5:
            messages.error(req, "Kullanıcı adı ve şifre 5 karakterden büyük olmalıdır")
            return render(req, "account/register.html")

        if password != repassword:
            messages.error(req, "Şifreler eşleşmiyor")
            return render(req, "account/register.html")

        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(req, "Kayıt başarılı! Giriş yapabilirsiniz.")
        return redirect("index")

    return render(req, "account/register.html")


def user_logout(req):
    logout(req)
    messages.success(req, "Çıkış Başarılı")
    return redirect("index")
