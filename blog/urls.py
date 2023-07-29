from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views



urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('blogging/', views.blogging, name='blog-blogging'),
    path('contact/', views.contact, name='blog-contact'),
    path('category/', views.category, name='blog-category'),
    path("single/<str:slug>/", views.single, name="blog-single"),
    path('tinymce/',include('tinymce.urls')),
    path('new_post/', views.new_post, name='new_post'),
    path("Update_post/<str:slug>/", views.updatePost, name='update'), 
    path("delete_post/<str:slug>/", views.deletePost, name='delete'), 
    path('login/', views.login, name='login'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

   
 