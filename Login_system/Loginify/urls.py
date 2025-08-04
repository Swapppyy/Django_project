from django.urls import path
from .views import (
    home,
    login_page,
    signup_page,
    get_all_users,
    get_user_by_username,
    update_user,
    delete_user,
)

urlpatterns = [
    path('home/', home),
    path('login/', login_page, name='login'),
    path('signup/', signup_page, name='signup'),

    path('api/users/', get_all_users, name='get_all_users'), 
    path('api/users/<str:username>/', get_user_by_username, name='get_user_by_username'), 
    path('api/users/update/<str:username>/', update_user, name='update_user'),  
    path('api/users/delete/<str:email>/', delete_user, name='delete_user'),  
]
