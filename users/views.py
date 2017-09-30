from hashlib import sha256 as hashed

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View
from wzwz_ru.settings import SITE_URL as www

from .forms import UserLoginForm, UserRegisterForm
from .models import User

app_name = 'users'


class UsersLoginFormView(View):
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get(self, request):
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
                messages.info(request, _("You are login as "
                                         "{}".format(full_name)))
                return redirect('/')
            else:
                messages.error(request, _("User does not found"))
                return render(request, self.template_name, args)

        else:
            # print('errors: ', form.errors.as_data())
            return render(request, self.template_name, args)


class RegisterUserView(View):
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def get(self, request):
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
                try:
                    new_user = User.objects.filter(email=email).first()
                    user_code = hashed((new_user.email
                                        + new_user.password).encode('utf-8')
                                       ).hexdigest()
                    subject = _('Registration on Web Zoomer')
                    message = _("You was registered on Web Zoomer"
                                "For activation yor account click follow link:"
                                " {}/users/activate/{}/{}"
                                "".format(www, new_user.id, user_code))
                    from_email = 'info@wzwz.ru'
                    try:
                        send_mail(subject, message, from_email, [email])
                        return redirect('/')
                    except BadHeaderError:
                        messages.error(request, _("Sending an email for you, "
                                                  "has failed. <a "
                                                  "href='/contact/'>Contact"
                                                  "</a> the administration"))
                        return render(request, self.template_name, args)
                except Exception as e:
                    print(e)
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
            print(user.is_active)
            user.is_active = True
            print(user.is_active)
        else:
            messages.error(request, _("Invalid verification code"))
    else:
        messages.error(request, _("User doesn't found"))
    return render(request, 'users/activate.html')


def logout_view(request):
    logout(request)
    return redirect('/')
