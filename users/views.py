# encoding: utf-8
from hashlib import sha256 as hashed
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import translation
from django.utils.translation import ugettext_lazy as _, LANGUAGE_SESSION_KEY
from django.views.generic import View
from wzwz_ru.settings import SITE_URL

from .forms import UserLoginForm, UserRegisterForm
from .models import User, Action

app_name = 'users'


class UsersLoginFormView(View):
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get(self, request):
        if 'uid' in request.session:
            messages.warning(request, _("You are already logged in"))
            return redirect('/')
        args = dict()
        form = self.form_class(None)
        args['form'] = form
        args['form_title'] = _('Sign in')
        return render(request, self.template_name, args)

    def post(self, request):
        args = dict()
        form = self.form_class(request.POST)
        args['form'] = form
        args['form_title'] = _('Sign in')
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.filter(email=email).first()
            if user is not None and check_password(password, user.password):
                login(request, user)
                full_name = user.first_name + ' ' + user.last_name
                request.session['uid'] = user.id
                messages.info(request, _("You are login as ") + full_name)
                return redirect('/')
            else:
                messages.error(request, _("User does not found"))
                return render(request, self.template_name, args)

        else:
            return render(request, self.template_name, args)


class RegisterUserView(View):
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def get(self, request):
        if 'uid' in request.session:
            messages.warning(request, _("You are already logged in"))
            return redirect('/')
        args = {}
        form = self.form_class(None)
        args['form'] = form
        args['form_title'] = _('Create account')
        return render(request, self.template_name, args)

    def post(self, request):
        args = {}
        form = self.form_class(request.POST)
        args['form'] = form
        args['form_title'] = _('Create account')
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            if password == confirm_password:
                new_user = form.save(commit=False)
                new_user.password = make_password(password)
                new_user.save()
                lang = translation.get_language()
                translation.activate(lang)
                subject_str = 'Registration on Web Zoomer'
                message_str = _("You was registered on Web Zoomer"
                                "For activation yor account click follow link:"
                                ) + " {}/users/activate/{}/{}/"
                new_user = User.objects.filter(email=email).first() or None
                if new_user is None:
                    messages.error(request, _("Error with create user"))
                    return render(request, self.template_name, args)
                user_code = hashed((new_user.email + new_user.password
                                    ).encode('utf-8')).hexdigest()
                subject = subject_str
                message = message_str.format(SITE_URL, new_user.id,
                                             user_code)
                from_email = 'info@wzwz.ru'.encode('utf-8')
                try:
                    send_mail(subject, message, from_email, [email])
                    messages.info(request,
                                  _("A massage was sent to your email"))
                    return redirect('/')
                except BadHeaderError:
                    messages.error(request, _("Sending an email for you, "
                                              "has failed. Please <a "
                                              "href='/contacts/'>Contact"
                                              "</a> support"))
                    return render(request, self.template_name, args)

            return render(request, self.template_name, args)
        else:
            return render(request, self.template_name, args)


def user_activation(request, uid, code):
    uid = int(uid) or None
    if uid is not None:
        user = User.objects.filter(id=uid).first()
    else:
        user = None
    if user is not None:
        user_code = hashed((user.email + user.password).encode('utf-8')
                           ).hexdigest()
        if user_code == code:
            if user.is_active:
                messages.warning(request, _("Your account is already active"))
            else:
                user.is_active = True
                user.save(update_fields=['is_active'])
                messages.info(request, _("Your account was activated"))
            return redirect(reverse('users:login'))
        else:
            messages.error(request, _("Invalid verification code"))
    else:
        messages.error(request, _("User doesn't found"))
    return render(request, 'users/activate.html')


def get_language_code(request):
    if LANGUAGE_SESSION_KEY in request.session:
        return request.session[LANGUAGE_SESSION_KEY]
    else:
        return 'en'


class UserProfile(View):
    template_name = 'users/profile.html'

    def get(self, request, uid):
        args = dict()
        args['title'] = _("Profile")
        language = get_language_code(request)
        args['actions'] = Action.objects.filter(language=language) or None

        return render(request, self.template_name, args)


class UserAction(View):
    template_name = 'users/action.html'

    def get(self, request, slug):

        args = dict()
        if LANGUAGE_SESSION_KEY in request.session:
            language = request.session[LANGUAGE_SESSION_KEY]
        else:
            language = 'en'
        args['title'] = Action.objects.filter(
            language=language, slug=slug).first().name.capitalize() \
            or _("Action")
        args['actions'] = Action.objects.filter(language=language) or None
        return render(request, self.template_name, args)


def logout_view(request):
    logout(request)
    return redirect('/')
