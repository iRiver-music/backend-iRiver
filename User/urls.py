from django.urls import path, include
from . import views

app_name = 'User'
urlpatterns = [
#     path('test/', views.test123, name='test123'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/<str:uid>/', views.logout, name='logout'),
    path('my_playList/<str:uid>/', views.my_playlist, name='my_playList'),
    path('profile/<str:uid>/', views.profileget, name='profile'),
    path('user_setting', views.user_setting, name='user_setting'),
    path('user_eq', views.user_eq, name='user_eq'),
    path('profile/', views.profilepost, name='profile'),

    path('save_session/', views.save_session, name='save_session'),
    path('isLogin/', views.checklogin, name='testuser'),
    path('get_user_show_data/', views.getuserdata, name='get_user_show_data'),
    path('get_user_music_list/', views.get_user_music_list, name='get_user_music_list'),
    path('get_user_session/', views.get_user_session, name='get_user_session'),
]