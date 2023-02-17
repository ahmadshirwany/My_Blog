from . import views
from django.urls import path

urlpatterns = [
    path("", views.starting_page.as_view(), name="starting-page"),
    path("posts/", views.Posts.as_view(), name="posts-page"),
    path("posts/<slug:slug>", views.post_detail.as_view(), name="post-detail-page"),  # posts/my-first-post
    path("read_later", views.readlater_view.as_view(), name="read-later-page"),
    path("sign_up", views.Signup_view.as_view(), name="registaration-page"),
    path("Log_in", views.Login_view.as_view(), name="Log-in-page"),
    path("Log_out", views.logout_request, name="Log-out"),
    # path('Post_API', views.PostLanguageViewSet.as_view(), name='Post_API1'),
    # path('User_API', views.UserViewSet.as_view(), name='user_API1'),
    path('sent_email', views.send_email.as_view(), name='sent_email')
]
