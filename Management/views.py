from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView

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

            # all of this assigning could be a method
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

        # could be a get call
        course = get_object_or_404(Course, pk=course_id)

        # could be a Course From method??
        form = CourseEditForm(instance=course)
        context = {'course': course, 'form': form}
        return render(request, "main/Course/courseEdit.html", context)

    def post(self, request, course_id):

        # get method
        course = get_object_or_404(Course, pk=course_id)
        form = CourseEditForm(request.POST, instance=course)
        if form.is_valid():

            # save method
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

        # get all method
        course = Course.objects.all()
        context = {'courses': course, 'roleTemplate': userRole, 'message': "Course Successfully Deleted"}
        return render(request, "main/Course/courses.html", context)


class usersInCourse(View):
    def get(self, request, course_id):
        users = []
        course = Course.objects.get(courseID=course_id)
        usersToCourses = UsersToCourse.objects.filter(courseID=course_id)
        userRole = request.session['roleSession']

        for y in usersToCourses:
            users.append(y.getUser())

        sortedUsers = sorted(users, key=lambda user: (user.role, user.lName))
        # sortedUsers = sorted(users, key=lambda x: (x[6], x[2]))
        context = {'course': course, 'users': sortedUsers, 'roleTemplate': userRole}
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


class userToCourseDelete(View):

    def get(self, request, email_id, course_id):
        user = UsersToCourse.objects.filter(assignment=email_id, courseID=course_id)
        try:
            for x in user:
                x.removeUser()

        except:

            not isinstance(user, UsersToCourse)

        # Redirect to a success page or back to the list of courses

        return redirect("usersInCourse", course_id=course_id)


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

        # could be a get method
        section = get_object_or_404(Section, pk=section_id)
        form = SectionForm(request.POST, instance=section)
        if form.is_valid():

            # could be a set method
            form.courseID = course_id
            form.save()
            return redirect('sections', course_id=course_id)
        else:
            context = {'section': section, 'form': form}
            return render(request, "main/Section/sectionEdit.html", context)


class sectionDelete(View):
    def get(self, request, course_id, section_id):
        # could be a get and a delete method

        Section.objects.filter(sectionID=section_id).delete()
        # Redirect to a success page or back to the list of sections
        return redirect('sections', course_id=course_id)


class userAdd(View):
    def get(self, request):
        form = UserForm()
        return render(request, 'main/User/userAdd.html', {'form': form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():

            # could be set methods

            email = form.cleaned_data['email']
            fname = form.cleaned_data['fName']
            lname = form.cleaned_data['lName']
            password = form.cleaned_data['password']
            phone = form.cleaned_data['phone']
            role = form.cleaned_data['role']

            # Create a new User object with the extracted data
            user = User(email=email, fName=fname, lName=lname, password=password, phone=phone, role=role)
            user.save()

            # return HttpResponse('User added successfully')
            return render(request, 'main/User/userAdd.html', {'form': form, 'message': "User Successfully Added"})

        else:
            form = UserForm()

        return render(request, 'main/User/userAdd.html',
                      {'form': form, 'message': "Cannot use an email already owned by another user. "
                                                "Please enter a different email"})


class userEdit(View):
    def get(self, request, email_id):

        # could be a get method
        user = get_object_or_404(User, pk=email_id)
        form = UserForm(instance=user)
        context = {'user': user, 'form': form}
        return render(request, "main/User/userEdit.html", context)

    def post(self, request, email_id):

        # could be a get method
        user = get_object_or_404(User, pk=email_id)
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users')
        else:
            context = {'user': user, 'form': form}
            return render(request, "main/User/userEdit.html", context)


class users(ListView):
    model = User
    template_name = 'main/User/users.html'
    context_object_name = 'results'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        queryset = super().get_queryset()
        if query:
            queryset = queryset.filter(
                Q(fName__icontains=query) | Q(email__icontains=query) | Q(lName__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        userRole = self.request.session['roleSession']
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['roleTemplate'] = userRole
        return context


class userDelete(View):
    def get(self, request, email_id):
        # could be a delete method
        User.objects.filter(email=email_id).delete()
        # Redirect to a success page or back to the list of courses
        userRole = request.session['roleSession']
        user = Course.objects.all()
        # context = {'results': user, 'roleTemplate': userRole, 'message': "Account Successfully Deleted"}
        return render(request, "main/User/users.html")


class notificationSend(View):
    # I think down the road we may not need this. For example, when adding a user to course or section,
    # we can automate an email to be generated and sent, rendering this view(page) obsolete.
    def get(self, request):
        return render(request, "main/notificationSend.html", {})
