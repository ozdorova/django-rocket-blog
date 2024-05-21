
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core.cache import cache
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from edu_project.settings import DEFAULT_USER_IMAGE
from mainapp.models import ArticleModel

from .forms import (LoginUserForm, ProfileUserForm, RegisterUserForm,
                    UserPasswordChangeForm)


class RegisterUser(CreateView):
    title = 'Регистрация'
    selected = 5
    # класс представление для регистрации
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {
        'title': title,
        'selected': selected,
    }
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        u = form.save(commit=False)
        u.save()
        u.groups.add(Group.objects.get(name='user'))
        return super().form_valid(form)


class EditProfileUser(LoginRequiredMixin, UpdateView):
    # класс предстваление для профиля пользователя
    title = 'Редактирование Профиля'
    selected = 6
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/edit_profile.html'
    extra_context = {
        'title': title,
        'selected': selected,
        'default_image': DEFAULT_USER_IMAGE,
    }

    def get_success_url(self) -> str:
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class ProfileUser(LoginRequiredMixin, ListView):
    # класс предстваление для профиля пользователя
    paginate_by = 4
    title = 'Профиль'
    selected = 6
    template_name = 'users/profile.html'
    extra_context = {
        'title': title,
        'selected': selected,
        'default_image': DEFAULT_USER_IMAGE,
    }
    context_object_name = 'user_posts'

    def get_queryset(self):
        articles = cache.get('cache_user_articles')
        if not articles:
            articles = ArticleModel.objects.filter(author_id=self.request.user.id).select_related(
                'cat').select_related('author')  # .prefetch_related('comments')
            cache.set('cache_user_articles', articles, 10)
        return articles


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {
        'title': 'Авторизация'
    }
    success_url = reverse_lazy('users:profile')

#     from users.models import User

# In [3]: from django.contrib.auth.models import Permission
#    ...: from django.contrib.contenttypes.models import ContentType
#    ...: content_type = ContentType.objects.get_for_model(User)
#    ...: permission = Permission.objects.create(codename="social_auth", name="Social Auth",  content_type=content_type)
#     <!-- вход черех соц сети -->
# <!-- <a href="{% url 'social:begin' 'github' %}"><img src="/media/social-auth/github.png" alt="github" width="5%" height="5%"></a>
# <a href="{% url 'social:begin' 'vk-oauth2' %}"><img src="/media/social-auth/vk.png" alt="vk" width="5%" height="5%"></a> -->


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change_form.html'

