from django.shortcuts import render, redirect
from django.views import View
from .models import User


# Create your views here.
# Need to create a landing page after login
# replace temp paths with proper url

class Home(View):

    def get(self, request):
        return render(request, "main/home.html", {})

    def post(self, request):
        noSuchUser = False
        badPassword = False
        try:
            m = User.objects.get(name=request.POST['email'])
            badPassword = (m.password != request.POST['password'])
        except:
            noSuchUser = True
        if noSuchUser:
            return render(request, "home.html", {"message": "User does not exist"})
        elif badPassword:
            return render(request, "home.html", {"message": "bad password"})
        else:
            request.session["name"] = m.name
            return redirect("/main/")


class MainHome(View):

    def get(self,request):
        m = request.session["name"]
        return render(request, "main/mainHome.html", {"name": m})
