from django.urls import path
from . import views

urlpatterns=[
    path('signup', views.signup, name="signup"),
    path('', views.homepage, name="homepage"),
    path('login', views.user_login, name="login"),
    path('logout', views.user_logout, name='logout'),
    path('generate-article', views.generate_article, name='generate-article'),
    path('blog_page', views.blog_pages, name="blog_page"),
    path('blogdetails', views.blog_details, name="blog_details"),
    
]