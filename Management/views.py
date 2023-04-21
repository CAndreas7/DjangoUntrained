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
            return render(request, "main/home.html", {"message": "Please enter a correct email and password."})
        elif badPassword:
            return render(request, "main/home.html", {"message": "bad password"})
        else:
            request.session["name"] = m.name
            return redirect("/main/maihHome.html")


class MainHome(View):

    def get(self,request):
        m = request.session["name"]
        return render(request, "main/mainHome.html", {"name": m})


class EditSections:
    def removeSection(self, param):
        pass

    def viewSection(self):
        pass

    def addSection(self, param, param1, param2, param3, param4, param5, param6):
        pass


def courses(request):
    return None


def courseEdit(request):
    return None


def editUserInCourse(request):
    return None