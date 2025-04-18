from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.ThemesOfForumView.as_view(), name='home'),
    path('forum/<int:forum_id>/', views.ThemesView.as_view(), name='themes'),
    path('theme/<int:theme_id>/', views.MessageView.as_view(), name='message'),
    path('profile/', views.profile_view, name="profile"),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('createForum', views.create_forum, name="createForum"),
    path('forum/<int:forum_id>/create_theme', views.create_theme, name="createTheme"),
]