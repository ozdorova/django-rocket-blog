
from django.contrib.auth.mixins import \
    LoginRequiredMixin  # PermissionRequiredMixin
from django.core.cache import cache
from django.db.models.base import Model
from django.http import HttpRequest, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  ListView, UpdateView)
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import ArticleForm, CommentsForm, ContactForm
from .models import ArticleModel, Comments
from .serializers import ArticleSerializer


@api_view(['GET'])
def article_api_view(request):
    articles = ArticleModel.objects.all()
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)


def chat(request, room_name):
    return render(
        request, 'mainapp/chat.html', {
            'room_name': room_name,
            'selected': 5,
            'title': 'Чат',
        }
    )


class HomeView(ListView):
    template_name = 'mainapp/index.html'
    selected = 1
    title = 'Главная'
    paginate_by = 4

    context_object_name = 'posts'
    extra_context = {
        'selected': selected,
        'title': title,
    }

    def get_queryset(self):
        articles = cache.get('cache_articles')
        if not articles:
            articles = ArticleModel.objects.filter(is_published=ArticleModel.Status.PUBLISHED).select_related(
                'cat').select_related('author')  # .prefetch_related('comments')
            cache.set('cache_articles', articles, 10)
        return articles


def comment(request, post_slug):
    pass


def about(request):
    extra_context = {
        'title': 'О блоге',
        'selected': 2,
    }
    return render(request, 'mainapp/about.html', context=extra_context)


class ShowPost(DetailView):
    template_name = 'mainapp/post.html'
    selected = 0
    title = 'Главная'

    slug_url_kwarg = 'post_slug'

    context_object_name = 'post'

    extra_context = {
        'selected': selected,
        'title': title,
    }

    def get_object(self, queryset=None) -> Model:
        return get_object_or_404(ArticleModel.published.select_related('author', 'cat'), slug=self.kwargs[self.slug_url_kwarg])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentsForm()
        return context


class BaseCommentView:
    model = Comments

    pk_url_kwarg = 'pk'

    def get_success_url(self):
        post = ArticleModel.objects.get(slug=self.object.article.slug)
        return reverse('show_post', kwargs={'post_slug': post.slug})

    def get_object(self, queryset=None):
        return get_object_or_404(Comments.objects.select_related('author', 'article',),
                                 pk=self.kwargs[self.pk_url_kwarg])


class AddCommentView(BaseCommentView, CreateView):
    form_class = CommentsForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.article = ArticleModel.objects.get(
            slug=self.kwargs['post_slug'])
        form.save()
        return redirect('show_post', post_slug=self.kwargs['post_slug'])

    def form_invalid(self, form):
        form.add_error(None, 'Ошибка')
        return redirect('show_post', post_slug=self.kwargs['post_slug'])


class EditCommentView(BaseCommentView, UpdateView):
    form_class = CommentsForm
    template_name = 'mainapp/comment_edit.html'


class DeleteCommentView(BaseCommentView, DeleteView):
    template_name = 'mainapp/comment_delete.html'


class AddPost(LoginRequiredMixin, CreateView):
    title = 'Добавить пост'
    selected = 4
    template_name = 'mainapp/addpost.html'
    success_url = reverse_lazy('users:profile')
    form_class = ArticleForm

    extra_context = {
        'selected': selected,
        'title': title,
    }

    def form_valid(self, form):
        a = form.save(commit=False)
        a.author = self.request.user
        a.cat_id = self.request.POST['cat']
        a.save()
        return super().form_valid(form)


class ContactView(LoginRequiredMixin, FormView):
    title = 'Обратная связь'
    selected = 3
    form_class = ContactForm
    template_name = 'mainapp/contact.html'
    success_url = reverse_lazy('home')

    extra_context = {
        'selected': selected,
        'title': title,
    }


def contact(request):
    extra_context = {
        'title': 'Обратная связь',
        'selected': 3,
    }
    return render(request, 'mainapp/contact.html', context=extra_context)


def show_post(request):
    return render(request, 'mainapp/post.html', context={'title': 'Смореть пост'})


# class ShowCategory(ListView):
#     template_name = 'mainapp/index.html'
#     selected = 1
#     title = 'Главная'
#     allow_empty = False
#     context_object_name = 'posts'

#     slug_url_kwarg = 'cat_slug'

#     def get_queryset(self):
#         return ArticleModel.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat').prefetch_related('comments')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = self.title
#         context['selected'] = self.selected
#         return context


def page_not_found(request: HttpRequest, exception) -> HttpResponseNotFound:
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
