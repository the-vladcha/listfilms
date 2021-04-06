from django.shortcuts import render, get_object_or_404

from .models import Film, Category, MyUser
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from listfilm.settings import EMAIL_HOST_USER
from .forms import LoginForm, RegistrationForm

from .models import MyUser

from django.urls import reverse
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import account_activation_token


def index(request):
    films = Film.objects.order_by('rating')
    categories = Category.objects.all()
    context = {
        'films': films,
        'title': 'Список фильмов',
        'categories': categories,
    }
    return render(request, template_name='fseen/index.html', context=context)


def get_category(request, slug):
    category_id = Category.objects.get(slug=slug).pk
    films = Film.objects.filter(category_id=category_id)
    # category = Category.objects.get(category_id=category_id)
    return render(request, 'fseen/category.html', {'films': films})


def view_film(request, slug):
    # film_item = Film.objects.get(slug=slug)
    film_item = get_object_or_404(Film, slug=slug)
    return render(request, 'fseen/view_film.html', {'film_item': film_item})


class LoginView(View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {'form': form}
        return render(request, 'fseen/login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
        context = {'form': form}
        return render(request, 'fseen/login.html', context)


class RegistrationView(View):
    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {'form': form}
        return render(request, 'fseen/register.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.is_active = False
            new_user.save()
            MyUser.objects.create(
                user=new_user,
                phone_number=form.cleaned_data['phone_number'],
            )

            # user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            # login(request, user)

            domain = get_current_site(request).domain
            uidb64 = urlsafe_base64_encode(force_bytes(new_user.pk))

            link = reverse('activate',
                           kwargs={'uidb64': uidb64, 'token': account_activation_token.make_token(new_user)})
            activate_url = 'http://' + domain + link
            email_subject = 'Подтверждение аккаунта'
            email_body = 'Привет ' + new_user.username + ' . Чтобы подтвердить регистарацию - перейдите по ссылке:\n' + activate_url
            email = EmailMessage(
                email_subject,
                email_body,
                EMAIL_HOST_USER,
                [new_user.email],
            )
            email.send(fail_silently=False)
            return redirect('home')
        context = {'form': form}
        return render(request, 'fseen/register.html', context)


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('home' + '?message=' + 'Пользователь уже подтвержден')

            if user.is_active:
                return redirect('home')
            user.is_active = True
            user.save()

            return redirect('home')

        except Exception as ex:
            pass
        return redirect('home')
