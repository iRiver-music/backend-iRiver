from django.urls import path, include
from . import views

app_name = 'user'
urlpatterns = [
#     path('test/', views.test123, name='test123'),
    path('save_session/', views.save_session, name='save_session'),
    path('register/', views.signup, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('isLogin/', views.checklogin, name='testuser'),
    path('profile2/', views.profile2, name='profile2'),
    path('get_user_show_data/', views.getuserdata, name='get_user_show_data'),
    path('get_user_music_list/', views.get_user_music_list, name='get_user_music_list'),
    # data
    path('get_user_session/', views.get_user_session, name='get_user_session'),
    # sql 操作get_user_session
    path('user_setting/', views.user_setting, name='user_setting'),
    path('user_eq/', views.user_eq, name='user_eq'),
]
