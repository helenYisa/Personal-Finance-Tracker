from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('delete-category/', views.delete_category, name='delete_category'),
    path('expenses/', views.expenses, name='expenses'),
    path('income/', views.income, name='income'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-category/', views.add_category, name='add_category'),
]
