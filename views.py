from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import (
    login_required,
    permission_required,
    user_passes_test,
)
from django.urls import reverse_lazy, reverse
from django.views import View
from .models import Profile
from django import forms


class AboutMeView(ListView):
    model = Profile
    template_name = "myauth/about-me.html"


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy("myauth:about-me")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user=user)
        return response


class UserListView(ListView):
    model = User
    template_name = "myauth/list_user.html"  # Укажите путь к вашему шаблону
    context_object_name = "users"  # Имя объекта в контексте

    def get_queryset(self):
        user_id = self.kwargs.get("id")  # Получите ID пользователя из URL
        if user_id:
            return User.objects.filter(id=user_id)  # Фильтруйте по ID
        return User.objects.all()  # Если ID не указан, возвращайте всех пользователей


class UserUpdateViev(UpdateView):
    """
    Для отображения детально конкретного юзера
    """

    model = User
    template_name = "myauth/user-update.html"
    context_object_name = "profile"
    fields = (
        "username",
        "first_name",
        "last_name",
    )
    success_url = reverse_lazy("myauth:about-me")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Получаем профиль, связанный с пользователем (если он есть)
        profile, created = Profile.objects.get_or_create(user=self.get_object())

        # Добавляем поля из модели Profile в форму
        form.fields["bio"] = forms.CharField(
            initial=profile.bio if profile else "", required=False
        )
        form.fields["avatar"] = forms.ImageField(
            initial=profile.avatar if profile else None, required=False
        )  # Поле для загрузки аватара

        return form

    def form_valid(self, form):
        # Сначала сохраняем изменения пользователя
        user = super().form_valid(form)

        # Получаем или создаем профиль
        profile, created = Profile.objects.get_or_create(user=self.get_object())

        # Обновляем профиль с новыми данными из формы
        profile.bio = form.cleaned_data.get("bio")

        # Обновляем аватар, если он был загружен
        if "avatar" in form.cleaned_data and form.cleaned_data["avatar"]:
            profile.avatar = form.cleaned_data["avatar"]

        profile.save()

        return user


@user_passes_test(lambda u: u.is_superuser, login_url=reverse_lazy("myauth:login"))
def set_cookie_viev(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response


def get_cookie_viev(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default value")
    return HttpResponse(f"Cookie value: {value!r}")


@permission_required("myauth.view_profile", raise_exception=True)
def set_session_viev(request: HttpRequest) -> HttpResponse:
    request.session["foobar"] = "spameggs"
    return HttpResponse("Session set")


@login_required
def get_session_viev(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foobar", "default value")
    return HttpResponse(f"Session value: {value!r}")


class FooBarYou(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({"foo": "bar", "spam": "eggs"})
