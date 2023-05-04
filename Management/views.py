from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import User, Section, Course, UsersToCourse
from .forms import SectionForm, CourseForm, UserForm, UserToFrom, CourseEditForm


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
            user = request.POST['email']
            password = request.POST['password']
            m = User.objects.get(email=request.POST['email'])
            badPassword = (m.password != request.POST['password'])
        except:
            noSuchUser = True
        if user == '' and password == '':
            return render(request, "main/home.html", {"message": "Email and password required."})
        elif user == '':
            return render(request, "main/home.html",
                          {
                              "password": password,
                              "message": "Email required."
                          })
        elif password == '':
            return render(request, "main/home.html",
                          {
                              "person": user,
                              "message": "Password required."
                          })
        elif noSuchUser:
            return render(request, "main/home.html", {"message": "Please enter a correct email and password."})
        elif badPassword:
            return render(request, "main/home.html",
                          {
                              "message": "Incorrect Password",
                              "person": user
                          })
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


class courses(View):
    def get(self, request):
        userRole = request.session['roleSession']
        course = Course.objects.all()
        context = {'courses': course, 'roleTemplate': userRole}
        return render(request, "main/Course/courses.html", context)


class courseAdd(View):

    def get(self, request):
        form = CourseForm()
        return render(request, 'main/Course/courseAdd.html', {'form': form})

    def post(self, request):

        form = CourseForm(request.POST)
        if form.is_valid():
            courseID = form.cleaned_data['courseID']
            courseName = form.cleaned_data['courseName']
            courseDescription = form.cleaned_data['courseDescription']
            courseDepartment = form.cleaned_data['courseDepartment']

            # Create a new Course object with the extracted data
            course = Course(courseID=courseID, courseName=courseName, courseDescription=courseDescription,
                            courseDepartment=courseDepartment)

            # Save the new course to the database
            course.save()

            return render(request, 'main/Course/courseAdd.html',
                          {'form': form, 'message': "Course Successfully added!"})
        else:
            form = CourseForm()

        return render(request, 'main/Course/courseAdd.html', {'form': form})


class courseEdit(View):
    def get(self, request, course_id):
        course = get_object_or_404(Course, pk=course_id)
        form = CourseEditForm(instance=course)
        context = {'course': course, 'form': form}
        return render(request, "main/Course/courseEdit.html", context)

    def post(self, request, course_id):
        course = get_object_or_404(Course, pk=course_id)
        form = CourseEditForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return render(request, 'main/Course/courseEdit.html',
                              {'form': form, 'message': "Course was successfully edited!"})
        else:
            context = {'course': course, 'form': form, 'message': "Cannot reuse the same ID."}
            return render(request, "main/Course/courseEdit.html", context)


class courseDelete(View):

    def get(self, request, course_id):
        Course.objects.filter(courseID=course_id).delete()
        # Redirect to a success page or back to the list of courses
        userRole = request.session['roleSession']
        course = Course.objects.all()
        context = {'courses': course, 'roleTemplate': userRole, 'message': "Course Successfully Deleted"}
        return render(request, "main/Course/courses.html", context)


class usersInCourse(View):
    def get(self, request, course_id):
        course = Course.objects.get(courseID=course_id)
        users = UsersToCourse.objects.filter(courseID=course_id)
        context = {'course': course, 'users': users}
        return render(request, 'main/UserToCourse/courseUsers.html', context)


class userToCourseAdd(View):

    def get(self, request, course_id):
        form = UserToFrom()
        return render(request, 'main/UserToCourse/courseUsersAdd.html', {'form': form, 'course_id': course_id})

    def post(self, request, course_id):
        form = UserToFrom(request.POST)

        if form.is_valid():
            try:
                email = form.cleaned_data['assignment']

                userTo = UsersToCourse(courseID=course_id, assignment=email)
                userTo.save()

                return redirect('usersInCourse', course_id=course_id)
            except Exception as e:
                print(e)
        else:
            print('Form is not valid')
            print(form.errors)
            form = UserToFrom()

        return render(request, 'main/UserToCourse/courseUsersAdd.html', {'form': form, 'course_id': course_id})

class editUserInCourse(View):

    def get(self, request):
        return render(request, "main/UserToCourse/editUserInCourse.html", {})


class sections(View):
    def get(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        sections = Section.objects.filter(courseID=course)
        context = {'course': course, 'sections': sections}
        return render(request, 'main/Section/sections.html', context)


class sectionAdd(View):
    def get(self, request, course_id):
        form = SectionForm(initial={'courseID': course_id})
        return render(request, 'main/Section/addSection.html', {'form': form, 'course_id': course_id})

    def post(self, request, course_id):
        form = SectionForm(request.POST)
        if form.is_valid():
            courseID = course_id
            location = form.cleaned_data['location']
            startTime = form.cleaned_data['startTime']
            endTime = form.cleaned_data['endTime']
            capacity = form.cleaned_data['capacity']
            TA = form.cleaned_data['TA']
            sectionID = form.cleaned_data['sectionID']

            # Create a new Section object with the extracted data
            section = Section(sectionID=sectionID, location=location, startTime=startTime, capacity=capacity, TA=TA,
                              courseID=courseID, endTime=endTime)
            section.save()

            return redirect('sections', course_id=course_id)
        else:
            form = SectionForm(initial={'courseID': course_id})

        return render(request, 'main/Section/addSection.html', {'form': form})


class sectionEdit(View):
    def get(self, request, section_id, course_id):
        section = get_object_or_404(Section, pk=section_id)
        form = SectionForm(instance=section)
        context = {'section': section, 'form': form}
        return render(request, "main/Section/sectionEdit.html", context)

    def post(self, request, section_id, course_id):
        section = get_object_or_404(Section, pk=section_id)
        form = SectionForm(request.POST, instance=section)
        if form.is_valid():
            form.courseID = course_id
            form.save()
            return redirect('sections', course_id=course_id)
        else:
            context = {'section': section, 'form': form}
            return render(request, "main/Section/sectionEdit.html", context)


class sectionDelete(View):
    def get(self, request, course_id, section_id):
        Section.objects.filter(sectionID=section_id).delete()
        # Redirect to a success page or back to the list of sections
        return redirect('sections', course_id=course_id)


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
        course = Course(courseID=courseID, courseName=courseName, courseDescription=courseDesc,
                        courseDepartment=courseDept)
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
        section = Section(sectionID=sectionID, location=location, startTime=startTime, endTime=endTime,
                          capacity=capacity, TA=ta, courseID=courseID)
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


class users(View):
    def get(self, request):
        users = User.objects.all()
        context = {'users': users}
        return render(request, "main/Account/accountEdit.html", context)


class userAdd(View):
    def get(self, request):
        form = UserForm()
        return render(request, 'main/User/userAdd.html', {'form': form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            phone = form.cleaned_data['phone']
            role = form.cleaned_data['role']

            # Create a new User object with the extracted data
            user = User(email=email, password=password, phone=phone, role=role)
            user.save()

            #return HttpResponse('User added successfully')
            return render(request, 'main/User/userAdd.html', {'form': form, 'message': "User Successfully Added"})

        else:
            form = UserForm()

        return render(request, 'main/User/userAdd.html', {'form': form, 'message': "Cannot use an email already owned by another user. "
                                                                               "Please enter a different email"})


class userEdit(View):
    def get(self, request, email_id):
        user = get_object_or_404(User, pk=email_id)
        form = UserForm(instance=user)
        context = {'user': user, 'form': form}
        return render(request, "main/User/userEdit.html", context)

    def post(self, request, email_id):
        user = get_object_or_404(User, pk=email_id)
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users')
        else:
            context = {'user': user, 'form': form}
            return render(request, "main/User/userEdit.html", context)


class accountEdit(View):
    def get(self, request):
        return render(request, "main/Account/accountEdit.html", {})


class userDelete(View):
    def get(self, request, email_id):
        User.objects.filter(email=email_id).delete()
        # Redirect to a success page or back to the list of courses
        return redirect('users')


class notificationSend(View):
#I think down the road we may not need this. For example, when adding a user to course or section,
#we can automate an email to be generated and sent, rendering this view(page) obsolete.
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

