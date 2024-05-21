from django.urls import include, path
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', cache_page(60)(views.about), name='about'),
    path('addpost/', views.AddPost.as_view(), name='addpost'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='show_post'),
    path('comments/add/<slug:post_slug>/', views.AddCommentView.as_view(), name='add_comment'),
    path('comments/edit/<int:pk>/', views.EditCommentView.as_view(), name='edit_comment'),
    path('comments/delete/<int:pk>/', views.DeleteCommentView.as_view(), name='delete_comment'),
    path('api/articles/', views.article_api_view, name='api_articles'),
    path('chat/<str:room_name>/', views.chat, name='chat'),
]

