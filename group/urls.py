from django.urls import path
from . import views

app_name = 'group'

urlpatterns = [
    path('', views.home, name='home'),
    path('group/create/', views.create_group, name='create_group'),
    path('group/<int:group_id>/edit/', views.edit_group, name='edit_group'),
    path('groups/', views.group_list, name='group_list'),
    path('follow/<int:group_id>/', views.follow, name='group_follow'),
    path('unfollow/<int:group_id>/', views.unfollow, name='group_unfollow'),
    path('quesiton/<int:question_id>/', views.question_detail, name='question_detail'),
    path('add_question/<int:group_id>/', views.create_question, name='create_question'),
    path('add_comment/<int:question_id>/', views.add_comment, name='add_comment'),
path('group/<str:group_name>/<int:group_id>', views.group, name='group_page'),
]