from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^free_key_generate/', views.free_key_generate, name='free_key_generate'),
    url(r'^free_key_generate_ajax/', views.free_key_generate_ajax, name='free_key_generate_ajax'),
    url(r'^auth_key_register/', views.auth_key_register, name='auth_key_register'),
    url(r'^auth_key_generate_ajax/', views.auth_key_generate_ajax, name='auth_key_generate_ajax'),
    url(r'^product_license_detail/(?P<product_id>[0-9]+)/$', views.product_license_detail, name='product_license_detail'),
    url(r'^logout/$', views.logout, name='logout'),
]