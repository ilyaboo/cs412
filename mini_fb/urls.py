from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.ShowAllProfilesView.as_view(), name='show_all'),
    path('profile/<int:pk>', views.ShowProfilePageView.as_view(), name='show_profile'),
    path('create_profile', views.CreateProfileView.as_view(), name='create_profile'),
    path('profile/<int:pk>/create_status', views.CreateStatusMessageView.as_view(), name='create_status'),
    path('profile/<int:pk>/update', views.UpdateProfileView.as_view(), name='update_profile'),
    path('status/<int:pk>/delete', views.DeleteStatusMessageView.as_view(), name='delete_message'),
    path('status/<int:pk>/update', views.UpdateStatusMessageView.as_view(), name='update_message'),
    path('status/<int:pk>/add_images', views.AddStatusMessageImages.as_view(), name='update_message_images'),
    path('status/<int:pk>/delete_images', views.DeleteStatusMessageImagesView.as_view(), name='delete_message_images'),
    path('image/<int:pk>/delete', views.DeleteStatusMessageImageView.as_view(), name='delete_message_image'),
]