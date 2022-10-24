from django.urls import path

from .views import AdList, AdDetail, AdCreate, AdEdit, responses_to_author, ResponseSearch


urlpatterns = [
    path('', AdList.as_view(), name='list_ads'),
    path('<int:pk>/', AdDetail.as_view(), name='ad_details'),
    path('create/', AdCreate.as_view(), name='ad_create'),
    path('<int:pk>/edit/', AdEdit.as_view(), name='ad_edit'),
    path('responses1/', ResponseSearch.as_view(), name='responses_to_author1'),
    path('responses/', responses_to_author, name='responses_to_author'),
]
