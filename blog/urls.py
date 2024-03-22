from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('', views.home, name='home'),
    path('create/', views.create_post, name='create_post'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('subscription/', views.subscription_plans, name='subscription'),
    path('purchase/', views.purchase_subscription,
         name='purchase'),
]
