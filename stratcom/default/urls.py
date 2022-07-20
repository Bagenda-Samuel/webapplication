from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('login/', views.login_page, name="loginpage"),
    path('about/', views.about_page, name="aboutpage"),
    path('gallery/', views.gallery_page, name="gallerypage"),
    path('dashboard/', views.dashboard_page, name="dashboardpge"),
    path('logout/', views.logout_page, name="logout"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)