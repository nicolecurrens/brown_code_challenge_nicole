from django.contrib import admin
from django.urls import path
from bdr_api import views


urlpatterns = [
    ## main ---------------------------------------------------------
    path( 'info/', views.info, name='info_url' ),
    ## other --------------------------------------------------------
    path( '', views.root, name='root_url' ),
    path( 'admin/', admin.site.urls ),
    path( 'error_check/', views.error_check, name='error_check_url' ),
    path( 'version/', views.version, name='version_url' ),
    path(  'items/<id>/', views.item_detail, name='item_detail_url'),
    path(  'related/<id>', views.related_items, name='related_item_url')
]
