from idlelib.rpc import request_queue
from multiprocessing import context

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Model
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, View
from .models import Profile

from accounts.forms import UserRegistrationForm, UserEditForm, ProfileEditForm


# from django.shortcuts import render
# from django.http import HttpResponse
# from django.contrib.auth import authenticate, login
# from .forms import LoginFrom
#
# # Create your views here.
#
# def user_login(request):
#     if request.method == "POST":
#         form = LoginFrom(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#             user = authenticate(request,
#                                 username=data['username'],
#                                 password=data['password'])
#             print(user)
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse('You logged in successfully!')
#                 else:
#                     return HttpResponse('Your profile is inactive!')
#
#             else:
#                 return HttpResponse('Login or password is incorrect!')
#
#     else:
#         form = LoginFrom()
#         context = {
#             'form':form
#         }
#     return render(request, 'registration/login.html', context)

class LogoutConfirmView(TemplateView):
    template_name = "registration/logged_out.html"

@login_required
def dashboard_view(request):
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)
    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'pages/user_profile.html', context)

def user_register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data["password"]
            )
            new_user.save()
            Profile.objects.create(user=new_user)
            context = {
                "new_user": new_user
            }
            return render(request, 'account/register_done.html', context)
    else:
        user_form = UserRegistrationForm()
        context = {
            'user_form':user_form
        }
        return render(request, 'account/register.html', context)


# class SignUpView(CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'account/register.html'

# def edit_user(request):
#     if request.method == 'POST':
#         user_form = UserEditForm(instance=request.user, data=request.POST)
#         profile_form = ProfileEditForm(instance=request.user.profile,
#                                        data=request.POST,
#                                        files=request.FILES)
#
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#         else:
#             user_form = UserEditForm(instance=request.user)
#             profile_form = ProfileEditForm(instance=request.user.profile)
#
#         return render(request, 'account/edit_profile.html', {"user_form":user_form, "profile_form":profile_form})


# @login_required
def edit_user(request):
    if request.method == "POST":
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'account/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})


class EditUserView(View):
    def get(self, request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request, 'account/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})

    def post(self, request):
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')