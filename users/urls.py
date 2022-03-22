from django.urls import path

from users.views import *

urlpatterns = [
    # path('login/', Login.as_view(), name='login'),
    # path('logout/', Logout.as_view(), name='logout'),
    # path('register/', Register.as_view(), name='register'),
    path('profile', UserPrfile.as_view(), name='profile'),
    path('operators', OperatorList.as_view(), name='operator-list'),
    # path('operator/<int:pk>/', OperatorList.as_view(), name='operator-list'),
    path('users', UserList.as_view(), name='user-list'),
    # path('user/<int:pk>/', UserList.as_view(), name='user-list'),
]
