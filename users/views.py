from __future__ import unicode_literals

from json import loads
from hashlib import sha256 as hashed
from httplib2 import Http
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
from requests import get as r_get

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import translation
from django.utils.translation import ugettext_lazy as _, LANGUAGE_SESSION_KEY
from django.utils.translation import get_language
from django.views.generic import View
from django.http import JsonResponse

from blog.models import Article
from main.functions import get_unique_str
from web_zoomer_com.settings import SITE_URL, BASE_DIR

from .forms import UserLoginForm, UserRegisterForm
from .models import User

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


class OAuthUserView(View):
    def post(self, request, provider):
        # STEP 1 - Parse the auth code
        code = request.data

        if provider == 'google':
            # STEP 2 - Exchange for a token
            try:
                # Upgrade the authorization code into a credentials object
                g_file = ''.join([BASE_DIR, '/client_secrets.json'])
                oauth_flow = flow_from_clientsecrets(g_file, scope='')
                oauth_flow.redirect_uri = 'postmessage'
                credentials = oauth_flow.step2_exchange(code)
            except FlowExchangeError:
                error = {'error': 'Failed to upgrade the authorization code.'}
                return JsonResponse(error)

            # Check that the access token is valid.
            access_token = credentials.access_token
            url = (
                'https://www.googleapis.com/oauth2/v1/tokeninfo'
                '?access_token=%s' %
                access_token)
            h = Http()
            result = loads(h.request(url, 'GET')[1])
            # If there was an error in the access token info, abort.
            if result.get('error') is not None:
                return JsonResponse({'error': 'server error'})

            # Get user info
            h = Http()
            userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
            params = {'access_token': credentials.access_token, 'alt': 'json'}
            answer = r_get(userinfo_url, params=params)

            data = answer.json()

            # see if user exists, if it doesn't make a new one
            user = User.objects.get(email=data['email']) or None
            if not user:
                user = User.objects.create_user(
                    username=data.get('name'),
                    avatar=data.get('picture'),
                    email=data.get('email'),
                    first_name=data.get('given_name'),
                    last_name=data.get('family_name'),
                    password=get_unique_str(8)
                )

            # Make token
            token = user.generate_auth_token()

            # Send back token to the client
            return JsonResponse({'token': token.decode('ascii'),
                                 'uid': user.id,
                                 'first_name': user.first_name,
                                 'last_name': user.last_name,
                                 'email': user.email,
                                 'picture': user.picture,
                                 'status': user.status,
                                 'full_name': user.get_full_name}), 200

        elif provider == 'facebook':

            data = request.json.get('data')
            access_token = data['access_token']
            fb_file = ''.join([BASE_DIR, '/facebook.json'])
            fb_data = loads(open(fb_file, 'r').read())['facebook']
            app_id = fb_data['app_id']
            app_secret = fb_data['app_secret']
            url = fb_data['access_token_url'] % (
                app_id, app_secret, access_token)
            h = Http()
            result = h.request(url, 'GET')[1]

            # Use token to get user info from API

            token = result.split(',')[0].split(':')[1].replace('"', '')
            url = fb_data['user_info_url'] % token

            h = Http()
            result = h.request(url, 'GET')[1]
            data = loads(result)
            name = data['name'].split(' ')

            user_data = dict()
            user_data['provider'] = 'facebook'
            user_data['username'] = data.get('name')
            user_data['first_name'] = name[0]
            user_data['last_name'] = name[1]
            user_data['email'] = data.get('email')
            user_data['facebook_id'] = data.get('id')
            user_data['access_token'] = token

            url = fb_data['picture_url'] % token
            h = Http()
            result = h.request(url, 'GET')[1]
            data = loads(result)
            user_data['picture'] = data['data']['url']
            # login_session['picture'] = data["data"]["url"]

            # see if user exists
            user_info = User.objects.get(user_data['email']) or None

            if user_info is None:
                user_info = User.objects.create(
                    username=user_data['username'],
                    password=get_unique_str(8),
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    email=user_data['email'],
                    avatar=user_data['picture'])

            g.user = user_info
            token = g.user.generate_auth_token()
            return JsonResponse({'token': token.decode('ascii'),
                                 'uid': g.user.id,
                                 'first_name': g.user.first_name,
                                 'last_name': g.user.last_name,
                                 'email': g.user.email,
                                 'picture': g.user.picture,
                                 'status': g.user.status,
                                 'full_name': g.user.get_full_name}), 200

        else:
            return JsonResponse({'error': 'Unknown provider'}), 200


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
        author = get_object_or_404(User, id=uid)
        args['title'] = _("Profile")
        args['author'] = author
        args['published_stories_by_author'] = Article.objects.filter(
            author=author).all().count()

        return render(request, self.template_name, args)

    def post(self, request, uid):
        if 'update_image' in request.POST:
            pass


def logout_view(request):
    logout(request)
    return redirect('/')
