from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import User, Section, Course
from .forms import SectionForm, CourseForm, UserForm
from django.urls import reverse


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
        userEmail = request.session["email"]

        try:
            thisUser = User.objects.get(pk=userEmail)
        except ValueError:
            thisUser = None

        userRole = thisUser.role
        request.session['roleSession'] = userRole
        return render(request, "main/mainHome.html", {"roleVariableTemplate": userRole})


class sections(View):
    def get(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        sections = Section.objects.filter(courseID=course)
        context = {'course': course, 'sections': sections}
        return render(request, 'main/sections.html', context)


class sectionAdd(View):
    def get(self, request, course_id):
        form = SectionForm(initial={'courseID': course_id})
        return render(request, 'main/addSection.html', {'form': form, 'course_id': course_id})

    def post(self, request, course_id):
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
            form = SectionForm(initial={'courseID': course_id})

        return render(request, 'main/addSection.html', {'form': form})


class sectionEdit(View):
    def get(self, request, section_id, course_id):
        section = get_object_or_404(Section, pk=section_id)
        form = SectionForm(instance=section) # change here
        context = {'section': section, 'form': form}
        return render(request, "main/sectionEdit.html", context)

    def post(self, request, section_id, course_id):
        section = get_object_or_404(Course, pk=section_id)
        form = SectionForm(request.POST, instance=section) # change here
        if form.is_valid():
            form.save()
            return redirect('sections', course_id=course_id)
        else:
            context = {'section': section, 'form': form}
            return render(request, "main/sectionEdit.html", context)

class sectionDelete(View):
    def get(self, request, course_id, section_id):
        Section.objects.filter(sectionID=section_id).delete()
        # Redirect to a success page or back to the list of sections
        return redirect('sections', course_id=course_id)


class courses(View):
    def get(self, request):
        userRole = request.session['roleSession']
        courses = Course.objects.all()
        context = {'courses': courses, 'roleTemplate': userRole}
        return render(request, "main/courses.html", context)


class courseEdit(View):
    def get(self, request, course_id):
        course = get_object_or_404(Course, pk=course_id)
        form = CourseForm(instance=course)
        context = {'course': course, 'form': form}
        return render(request, "main/courseEdit.html", context)

    def post(self, request, course_id):
        course = get_object_or_404(Course, pk=course_id)
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('courses')
        else:
            context = {'course': course, 'form': form}
            return render(request, "main/courseEdit.html", context)


class editUserInCourse(View):

    def get(self, request):
        return render(request, "main/editUserInCourse.html", {})


class accountEdit(View):
    def get(self, request):
        return render(request, "main/accountEdit.html", {})

class notificationSend(View):

    def get(self, request):
        # userEmail = request.session["email"]
        #
        # try:
        #     thisUser = User.objects.get(pk=userEmail)
        # except ValueError:
        #     thisUser = None
        #
        # roleVariableView = thisUser.role
        return render(request, "main/notificationSend.html", {})

class courseAdd(View):

    def get(self, request):

        return render(request, "main/courseAdd.html", {})


class MyUser(User):

    def __init__(self, email, password, phone, role):
        self.email = email
        self.password = password
        self.phone = phone
        self.role = role

    def addAccount(self, email, password, phone, role):
        user = User(email=email, password=password, phone=phone, role=role)
        user.save()

    def getEmail(self):
        return self.email

    def setEmail(self, email):
        users = User.objects.filter(email=self.email)
        for user in users:
            user.email = email
            user.save()
        self.email = email

    def getPassword(self):
        return self.password

    def setPassword(self, password):
        passwords = User.objects.filter(password=self.password)
        for word in passwords:
            word.password = password
            word.save()
        self.password = password

    def getPhone(self):
        return self.phone

    def setPhone(self, phoneNum):
        phones = User.objects.filter(phone=phoneNum)
        for item in phones:
            item.phone = phoneNum
            item.save()
        self.phone = phoneNum

    def editAccount(self, email, password, phoneNum, role):
        user = User.objects.filter(email=email)
        for item in user:
            item.password = password
            item.phone = phoneNum
            item.role = role
            item.save()
        self.password = password
        self.phone = phoneNum
        self.role = role

    def removeAccount(self, email):
        User.objects.filter(email=email).delete()
        self.email = None
        self.password = None
        self.phone = None
        self.role = None

    def addCourse(self, courseID, courseName, courseDesc, courseDept):
        course = Course(courseID=courseID, courseName=courseName, courseDescription=courseDesc, courseDepartment=courseDept)
        course.save()

    def editCourse(self, courseID, courseName, courseDescription, courseDepartment):
        courses = Course.objects.filter(courseID=courseID)
        for item in courses:
            item.courseName = courseName
            item.courseDescription = courseDescription
            item.courseDepartment = courseDepartment
            item.save()

    def removeCourse(self, courseID):
        Course.objects.filter(courseID=courseID).delete()

    def addSection(self, sectionID, location, startTime, endTime, capacity, ta, courseID):
        section = Section(sectionID=sectionID, location=location, startTime=startTime, endTime=endTime, capacity=capacity, TA=ta, courseID=courseID)
        section.save()

    def editSection(self, sectionID, location, startTime, endTime, capacity, ta, courseID):
        sections = Section.objects.filter(sectionID=sectionID)
        for item in sections:
            item.location = location
            item.startTime = startTime
            item.endTime = endTime
            item.capacity = capacity
            item.TA_id = ta
            item.courseID_id = courseID
            item.save()

    def removeSection(self, sectionID):
        Section.objects.filter(sectionID=sectionID).delete()


