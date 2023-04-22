from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import User, Section
from .forms import SectionForm


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
            m = User.objects.get(email=request.POST['email'])
            badPassword = (m.password != request.POST['password'])
        except:
            noSuchUser = True
        if noSuchUser:
            return render(request, "main/home.html", {"message": "Please enter a correct email and password."})
        elif badPassword:
            return render(request, "main/home.html", {"message": "bad password"})
        else:
            request.session["email"] = m.email
            return redirect("/main/")


class MainHome(View):

    def get(self, request):
        m = request.session["email"]
        return render(request, "main/mainHome.html", {"email": m})


class EditSections(View):

    def viewSection(self):
        # Return a QuerySet containing all sections in the database
        return Section.objects.all()

    def removeSection(self, section_id):
        # Delete the section with the given section_id from the database
        Section.objects.filter(sectionID=section_id).delete()

    def addSection(self, request):
        if request.method == 'POST':
            form = SectionForm(request.POST)
            if form.is_valid():
                courseID = form.cleaned_data['courseID']
                location = form.cleaned_data['location']
                startTime = form.cleaned_data['startTime']
                endTime = form.cleaned_data['endTime']
                capacity = form.cleaned_data['capacity']
                TA = form.cleaned_data['TA']
                sectionID = form.cleaned_data['sectionID']

                # Create a new Section object with the extracted data
                section = Section(courseID=courseID, location=location, startTime=startTime,
                                  endTime=endTime, capacity=capacity, TA=TA, sectionID=sectionID)

                # Save the new section to the database
                section.save()

                return HttpResponse('Section added successfully')
        else:
            form = SectionForm()

        return render(request, 'main/addSection.html', {'form': form})


class courses(View):
    def get(self, request):
        return render(request, "main/courses.html", {})


class courseEdit(View):
    def get(self, request):
        return render(request, "main/courseEdit.html", {})


class editUserInCourse(View):

    def get(self, request):
        return render(request, "main/editUserInCourse.html", {})
