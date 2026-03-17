from django.contrib import admin
from django.urls import path, include
from agenda.views.views_login import login_view, register_view, CustomLogoutView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth (sem namespace para que {% url 'login' %} e {% url 'logout' %} funcionem)
    path('login/', login_view, name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),

    # App principal
    path('', include('agenda.urls', namespace='cal')),
]
