from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from .email import Email
from .models import User, Section, Course, UsersToCourse
from .forms import SectionForm, CourseForm, UserForm, UserToFrom, CourseEditForm, SectionEditForm
from django.contrib.auth import logout


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
        if 'messageC' not in request.session:
            request.session['messageC'] = ""

        msg = request.session['messageC']
        request.session['messageC'] = ""

        userRole = request.session['roleSession']
        course = Course.objects.all()
        context = {'courses': course, 'roleTemplate': userRole, "message": msg}
        return render(request, "main/Course/courses.html", context)


class courseAdd(View):

    def get(self, request):
        form = CourseForm()
        return render(request, 'main/Course/courseAdd.html', {'form': form})

    def post(self, request):

        form = CourseForm(request.POST)
        if Course.formAdd(form):
            request.session['messageC'] = "Course Successfully added!"
            courses_view = courses()
            # return render(request, 'main/Course/courseAdd.html', {'form': form, 'message': "Course Successfully added!"})
            return courses_view.get(request)
        else:
            form = CourseForm()
        return render(request, 'main/Course/courseAdd.html', {'form': form,
                                                              'message': "Course ID is either already used or Invalid Form Data"})


class courseEdit(View):
    def get(self, request, course_id):

        course = Course.getCourse(course_id)

        form = CourseEditForm(instance=course)
        context = {'course': course, 'form': form}

        return render(request, "main/Course/courseEdit.html", context)

    def post(self, request, course_id):

        course = Course.getCourse(course_id)
        form = CourseEditForm(request.POST, instance=course)
        if course.formSave(form):
            request.session['messageC'] = "Course was successfully edited."

            # return render(request, 'main/Course/courseEdit.html', {'form': form, 'message': "Course was successfully edited!"})
            courses_view = courses()
            return courses_view.get(request)
        else:
            context = {'course': course, 'form': form, 'message': "Could not edit Course Information"}
            return render(request, "main/Course/courseEdit.html", context)


class courseDelete(View):

    def get(self, request, course_id):
        Course.objects.filter(courseID=course_id).delete()
        # Redirect to a success page or back to the list of courses
        userRole = request.session['roleSession']

        # get all method
        course = Course.objects.all()
        request.session['messageC'] = "Course was successfully deleted."

        context = {'courses': course, 'roleTemplate': userRole, 'message': "Course Successfully Deleted"}
        return render(request, "main/Course/courses.html", context)


class usersInCourse(View):
    def get(self, request, course_id):
        if 'messageUIC' not in request.session:
            request.session['messageUIC'] = ""
        msg = request.session['messageUIC']
        request.session['messageUIC'] = ""

        userList = []

        # Get method
        course = Course.getCourse(course_id)
        # get method
        usersToCourses = UsersToCourse.getUserInCourse(course_id)
        userRole = request.session['roleSession']

        for y in usersToCourses:
            userList.append(y.getUser())

        sortedUsers = sorted(userList, key=lambda user: (user.role, user.lName))
        context = {'course': course, 'users': sortedUsers, 'roleTemplate': userRole, "message": msg}
        return render(request, 'main/UserToCourse/courseUsers.html', context)


class userToCourseAdd(View):

    def get(self, request, course_id):
        form = UserToFrom()
        # need users in context to show people in the template to choose from
        user = User.objects.exclude(role=1)
        return render(request, 'main/UserToCourse/courseUsersAdd.html',
                      {'form': form, 'course_id': course_id, 'users': user})

    def post(self, request, course_id):
        form = UserToFrom(request.POST)
        email = form.clean_assignment()
        name = User.objects.get(pk=email).getfName()

        if UsersToCourse.addUserToCourse(email, course_id):
            Email.emailGen(name, email, course_id)
            request.session['messageUIC'] = "User successfully added to course."
            user_to_course_view = usersInCourse()
            return user_to_course_view.get(request, course_id)
            # return redirect('usersInCourse', course_id=course_id)
        else:
            user = User.objects.all()
            return render(request, 'main/UserToCourse/courseUsersAdd.html',
                          {'form': form, 'course_id': course_id, 'users': user, 'message': "User already exists!"})


class userToCourseDelete(View):

    def get(self, request, email_id, course_id):
        user = UsersToCourse.objects.filter(assignment=email_id, courseID=course_id)
        try:
            for x in user:
                x.delete()
        except:
            not isinstance(user, UsersToCourse)
        request.session['messageUIC'] = "User successfully deleted."

        # Redirect to a success page or back to the list of courses

        # return redirect("usersInCourse", course_id=course_id)
        user_to_course_view = usersInCourse()
        return user_to_course_view.get(request, course_id)


class sections(View):
    def get(self, request, course_id):
        if 'messageS' not in request.session:
            request.session['messageS'] = ""

        msg = request.session['messageS']
        request.session['messageS'] = ""

        # get method
        course = Course.getCourse(course_id)
        # get method
        sectionList = Section.getSectionsFromCourse(course_id)
        userRole = request.session['roleSession']
        context = {'course': course, 'sections': sectionList, 'roleTemplate': userRole, "message": msg}
        return render(request, 'main/Section/sections.html', context)


class sectionAdd(View):
    def get(self, request, course_id):
        form = SectionForm(initial={'courseID': course_id})
        user = User.objects.all()

        if 'messageS_invalid_form' in request.session:
            context = {'form': form, 'course_id': course_id, 'people': user,
                       'message': request.session['messageS_invalid_form']}
            return render(request, 'main/Section/addSection.html', context)

        return render(request, 'main/Section/addSection.html', {'form': form, 'course_id': course_id, 'people': user,
                                                                })

    def post(self, request, course_id):
        form = SectionForm(request.POST)
        if Section.formAdd(form, course_id):
            request.session['messageS'] = "Section successfully added."

            # return redirect('sections', course_id=course_id)
            sections_view = sections()
            return sections_view.get(request, course_id)
        else:
            form = SectionForm(initial={'courseID': course_id})
            sectionsAdd_view = sectionAdd()

            request.session['messageS_invalid_form'] = "Section ID is either already used or Invalid Form Data"

        return sectionsAdd_view.get(request, course_id)


class sectionEdit(View):
    def get(self, request, section_id, course_id):
        section = Section.getSection(section_id)
        user = User.objects.all()
        form = SectionEditForm(instance=section, initial={'courseID': course_id})
        context = {'section': section, 'form': form, 'course_id': course_id, 'people': user}
        return render(request, "main/Section/sectionEdit.html", context)

    def post(self, request, section_id, course_id):

        # could be a get method
        section = Section.getSection(section_id)
        form = SectionEditForm(request.POST)
        if section.formSave(form):
            request.session['messageS'] = "Section successfully edited."

            # return redirect('sections', course_id=course_id)

            sections_view = sections()
            return sections_view.get(request, course_id)
        else:
            context = {'section': section, 'form': form}
            return render(request, "main/Section/sectionEdit.html", context)


class sectionDelete(View):
    def get(self, request, course_id, section_id):
        # could be a get and a delete method

        Section.deleteSection(section_id)
        request.session['messageS'] = "Section successfully deleted."

        # Redirect to a success page or back to the list of sections
        # return redirect('sections', course_id=course_id)
        sections_view = sections()
        return sections_view.get(request, course_id)


class userAdd(View):
    def get(self, request):
        form = UserForm()
        return render(request, 'main/User/userAdd.html', {'form': form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():

            # could be set methods

            User.formAdd(form)
            # request.session['messageU'] = "Account successfully created."

            # return HttpResponse('User added successfully')
            return render(request, 'main/User/userAdd.html', {'form': form, 'message': "User Successfully Added"})

        else:
            form = UserForm()

        return render(request, 'main/User/userAdd.html',
                      {'form': form, 'message': "Email is either already used or Invalid Form Data"})


class userEdit(View):
    def get(self, request, email_id):

        # could be a get method
        user = User.getUser(email_id)
        form = UserForm(instance=user)
        context = {'user': user, 'form': form}
        return render(request, "main/User/userEdit.html", context)

    def post(self, request, email_id):

        # could be a get method
        user = User.getUser(email_id)
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            if email_id != form.cleaned_data['email']:
                User.deleteUser(email_id)
            form.save()
            request.session['messageU'] = "User Edited."
            return redirect('users')
        else:
            context = {'user': user, 'form': form, "message": "Something went wrong."}
            return render(request, "main/User/userEdit.html", context)


# I feel like i could break this into a search class somehow
class users(ListView):
    model = User
    template_name = 'main/User/users.html'
    context_object_name = 'results'

    # if 'messageU' not in request.session:
    #     request.session['messageU'] = ""
    #
    # msg = request.session['messageU']
    # request.session['messageU'] = ""

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        queryset = super().get_queryset()
        if query:
            queryset = queryset.filter(
                Q(fName__icontains=query) | Q(email__icontains=query) | Q(lName__icontains=query)
                | Q(phone__icontains=query) | Q(role__icontains=query))
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
        User.deleteUser(email_id)
        # Redirect to a success page or back to the list of courses
        userRole = request.session['roleSession']
        user = User.objects.all()
        # request.session['messageU'] = "Account successfully deleted."

        context = {'results': user, 'roleTemplate': userRole, 'message': "Account Successfully Deleted"}
        return render(request, "main/User/users.html", context)


def userLogout(request):
    logout(request)
    return redirect('login')
