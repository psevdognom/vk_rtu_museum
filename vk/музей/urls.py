from django.urls import path
from .views import *
from museum.settings import MEDIA_ROOT, MEDIA_URL, DEBUG
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', main_view, name = 'main'),
    path('место/создать/', PlaceCreate.as_view(), name = 'place_create_url'),
    path('место/<str:slug>/', place_detail, name = 'place_detail_url'),
    path('место/<str:slug>/удалить/', PlaceDelete.as_view(), name = 'place_delete_url'),
    path('место/<str:slug>/изменить/', PlaceUpdate.as_view(), name = 'place_update_url'),
    path('категория/создать/', CategoryCreate.as_view(), name = 'category_create_url'),
    path('категория/<str:slug>/', category_detail, name='category_detail_url'),
    path('категория/<str:slug>/удалить/', CategoryDelete.as_view(), name = 'category_delete_url'),
    path('категория/<str:slug>/изменить/', CategoryUpdate.as_view(), name = 'category_update_url'),
    path('экспонат/создать/', new_item_create, name = 'item_create_url'),
    path('экспонат/<str:slug>/удалить/', ItemDelete.as_view(), name='item_delete_url'),
    path('экспонат/<str:slug>/изменить/', ItemUpdate.as_view(), name='item_update_url'),
    path('экспонат/<str:slug>/', ItemDetail.as_view(), name='item_detail_url'),
]

urlpatterns += staticfiles_urlpatterns()
if DEBUG:
        urlpatterns += static(MEDIA_URL,
                              document_root=MEDIA_ROOT)