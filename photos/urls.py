from django.urls import path
from . import views
urlpatterns = [
    path('photos/', views.PhotoList.as_view(), name='photos'),
    path('photos/<int:pk>/', views.PhotoDetail.as_view(), name='photo_detail'),
]