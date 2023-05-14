from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from .email import Email
from .models import User, Section, Course, UsersToCourse
from .forms import SectionForm, CourseForm, UserForm, UserToFrom, CourseEditForm, SectionEditForm
from django.contrib.auth import logout
from importlib import import_module
from django.conf import settings

# Create your views here.
# Need to create a landing page after login
# replace temp paths with proper url

def getSession():
    SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
    return SessionStore()

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
            request.session["message"] = ""
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
        request.session['messageC'] = ''

        userRole = request.session['roleSession']
        course = Course.objects.all()
        context = {'courses': course, 'roleTemplate': userRole, 'message': msg}
        return render(request, "main/Course/courses.html", context)


class courseAdd(View):

    def get(self, request):
        form = CourseForm()
        return render(request, 'main/Course/courseAdd.html', {'form': form})

    def post(self, request):
        form = CourseForm(request.POST)
        if Course.formAdd(form):
            return render(request, 'main/Course/courseAdd.html',
                          {'form': form, 'message': "Course Successfully added!"})
        else:
            form = CourseForm()
        return render(request, 'main/Course/courseAdd.html',
                      {'form': form, 'message': "Error: Course ID Already Exists."})

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
            return render(request, 'main/Course/courseEdit.html',
                          {'form': form, 'message': "Course was successfully edited!"})

        else:
            context = {'course': course, 'form': form, "message": "Error: Something went wrong."}
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

        if 'messageUTC' not in request.session:
            request.session['messageUTC'] = ""
        msg = request.session['messageUTC']
        request.session['messageUTC'] = ""
        userList = []

        # Get method
        course = Course.getCourse(course_id)
        # get method
        usersToCourses = UsersToCourse.getUserToCourse(course_id)
        userRole = request.session['roleSession']

        for y in usersToCourses:
            userList.append(y.getUser())

        sortedUsers = sorted(userList, key=lambda user: (user.role, user.lName))
        context = {'course': course, 'users': sortedUsers, 'roleTemplate': userRole, 'message': msg}
        return render(request, 'main/UserToCourse/courseUsers.html', context)


class userToCourseAdd(View):

    def get(self, request, course_id):
        form = UserToFrom()
        return render(request, 'main/UserToCourse/courseUsersAdd.html', {'form': form, 'course_id': course_id})

    def post(self, request, course_id):
        form = UserToFrom(request.POST)
        email = form.clean_assignment()
        utcCheck = UsersToCourse.objects.filter(assignment=email, courseID=course_id)

        # Ensure user is not yet assigned to course
        if utcCheck.count() == 0 or utcCheck is None:
            UsersToCourse.addUserToCourse(email, course_id)
            # Send email notification
            name = User.objects.get(pk=email).getfName()
            Email.emailGen(name, email, course_id)
            request.session['messageUTC'] = "User Added to Course and Email Sent To User."
            return redirect('usersInCourse', course_id=course_id)
        else:
            msg = "That user is already assigned to this course."
            return render(request, 'main/UserToCourse/courseUsersAdd.html', {'form': form, 'course_id': course_id, 'message': msg})


class userToCourseDelete(View):

    def get(self, request, email_id, course_id):
        user = UsersToCourse.objects.get(assignment=email_id, courseID=course_id)
        user.removeUser()
        request.session['messageUTC'] = "User Removed."
        return redirect("usersInCourse", course_id=course_id)


class sections(View):
    def get(self, request, course_id):

        if 'messageS' not in request.session:
            request.session['messageS'] = ""
        msg = request.session['messageS']
        request.session['messageS'] = ''

        # get method
        course = Course.getCourse(course_id)
        # get method
        sectionList = Section.getSectionsFromCourse(course_id)
        context = {'course': course, 'sections': sectionList, 'message': msg}
        return render(request, 'main/Section/sections.html', context)


class sectionAdd(View):
    def get(self, request, course_id):
        form = SectionForm(initial={'courseID': course_id})
        return render(request, 'main/Section/addSection.html', {'form': form, 'course_id': course_id})

    def post(self, request, course_id):
        form = SectionForm(request.POST)
        if Section.formAdd(form, course_id):
            #This does not account for sections already existing within course
            request.session['messageS'] = "Section Added."
            return redirect('sections', course_id=course_id)
        else:
            form = SectionForm(initial={'courseID': course_id})
        return render(request, 'main/Section/addSection.html', {'form': form, "message": "Something went wrong."})


class sectionEdit(View):
    def get(self, request, section_id, course_id):
        section = Section.getSection(section_id)
        form = SectionEditForm(instance=section, initial={'courseID': course_id})
        context = {'section': section, 'form': form, 'course_id': course_id}
        return render(request, "main/Section/sectionEdit.html", context)

    def post(self, request, section_id, course_id):

        # could be a get method
        section = Section.getSection(section_id)
        form = SectionEditForm(request.POST)
        if section.formSave(form):
            request.session['messageS'] = "Section Edited."
            return redirect('sections', course_id=course_id)
        else:
            context = {'section': section, 'form': form, "message": "Something went wrong."}
            return render(request, "main/Section/sectionEdit.html", context)


class sectionDelete(View):
    def get(self, request, course_id, section_id):

        Section.deleteSection(section_id)
        request.session['messageS'] = "Section Deleted."
        return redirect('sections', course_id=course_id)


class userAdd(View):
    def get(self, request):
        form = UserForm()
        return render(request, 'main/User/userAdd.html', {'form': form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():

            # could be set methods

            User.formAdd(form)

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
        user = User.getUser(email_id)
        form = UserForm(instance=user)
        context = {'user': user, 'form': form}
        return render(request, "main/User/userEdit.html", context)

    def post(self, request, email_id):

        # could be a get method
        user = User.getUser(email_id)
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            request.session['messageU'] = "User Edited."
            return redirect('users')
        else:
            context = {'user': user, 'form': form, 'message': "Something went wrong."}
            return render(request, "main/User/userEdit.html", context)


# I feel like i could break this into a search class somehow
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
        User.deleteUser(email_id)
        UsersToCourse.delUserCourses(email_id)
        # Redirect to a success page or back to the list of courses
        userRole = request.session['roleSession']
        user = Course.objects.all()
        request.session['messageU'] = "User Deleted."

        context = {'results': user, 'roleTemplate': userRole, 'message': "Account Successfully Deleted"}
        return render(request, "main/User/users.html", context)


def userLogout(request):
    logout(request)
    return redirect('login')

