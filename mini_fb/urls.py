from django.urls import path
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.ShowAllProfilesView.as_view(), name='show_all'),
    path('profile/<int:pk>', views.ShowProfilePageView.as_view(), name='show_profile'),
    path('create_profile', views.CreateProfileView.as_view(), name='create_profile'),
    path('profile/create_status', views.CreateStatusMessageView.as_view(), name='create_status'),
    path('profile/update', views.UpdateProfileView.as_view(), name='update_profile'),
    path('status/<int:pk>/delete', views.DeleteStatusMessageView.as_view(), name='delete_message'),
    path('status/<int:pk>/update', views.UpdateStatusMessageView.as_view(), name='update_message'),
    path('status/<int:pk>/add_images', views.AddStatusMessageImages.as_view(), name='update_message_images'),
    path('status/<int:pk>/delete_images', views.DeleteStatusMessageImagesView.as_view(), name='delete_message_images'),
    path('image/<int:pk>/delete', views.DeleteStatusMessageImageView.as_view(), name='delete_message_image'),
    path('profile/add_friend/<int:other_pk>', views.CreateFriendView.as_view(), name='add_friend'),
    path('profile/friend_suggestions', views.ShowFriendSuggestionsView.as_view(), name='see_suggestions'),
    path('profile/news_feed', views.ShowNewsFeedView.as_view(), name='see_news'),
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='mini_fb/logged_out.html'), name='logout'),
]