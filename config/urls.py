from django.contrib import admin
from django.urls import include, path

from reviews import views

urlpatterns = [
    path('reviews/', include('reviews.urls')),
    path('authentication/', include('authentication.urls')),
    path('admin/', admin.site.urls),
]
